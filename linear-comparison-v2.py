"""linear-comparison-v2.py

CHANGELOG vs linear_comparison.py
- Moved the in-file Control Panel into adjacent YAML config loading.
- Added a normal single-file entrypoint with argparse and main().
- Sorted src/rip/flt discovery so pair ordering is deterministic.
- Kept crop_param src-only and added src_prefilter modes: none, ivtc, deinterlace.
- Removed FrameInfo/style text burn-in and now writes plain 8-bit RGB PNGs.
- Replaced sampled-clip concatenation plus set_output() with direct per-frame
  fpng.Write(...).get_frame(sample_idx) calls on the original clips.
- Renamed outputs to "{src stem} - {frame} - src|rip|flt.png".
- Derived frame-number padding from clip.num_frames, removing start_num/num_len.
- Added optional flt comparison via .vpy output 0 loading in dedicated helpers.
- rip_ext is now a single configured suffix, defaulting to .hevc.
- Added explicit cleanup around flt script loading and zero-frame guards.
- When sorted list lengths differ, truncates to the shortest list and requires
  explicit Y/y confirmation after printing the planned matches.
- Skips any .hevc rip pair whose rip has a sibling .hevc.busy or .hevc.break marker.
- Reformatted console output and added simple progress indicators.
- Added overwrite control plus default config discovery across local and
  platform-standard config directories.
- If no config is found, writes a default YAML beside the script and exits
  without generating comparison images.
- Switched console logging to compact fixed tags and ANSI colors with fallback.
"""

from __future__ import annotations

import argparse
import ctypes
import gc
import math
import os
import random
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import rksfunc as rks
import vapoursynth as vs
import yaml
from mvsfunc import ToRGB


core = vs.core

DEFAULT_CONFIG_NAME = "linear-comparison-config.yaml"
APP_CONFIG_DIR_NAME = "linear-comparison"
OUTPUT_WIDTH = 84
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
LEVEL_STYLES = {
    "INFO": "\033[36m",
    "WARN": "\033[33m",
    "ALERT": "\033[31m",
    "STOP": "\033[91m",
    "OK": "\033[32m",
    "SKIP": "\033[35m",
}


@dataclass(frozen=True)
class Config:
    config_path: Path
    input_dir: Path
    sample_itv: int
    random_seed: int | None
    crop_param: tuple[int, int, int, int]
    src_prefilter: int
    src_ext: str
    rip_ext: str
    compare_flt: bool
    flt_ext: str
    src_output_dir: Path
    rip_output_dir: Path
    flt_output_dir: Path
    overwrite: bool
    max_cache_size: int


@dataclass(frozen=True)
class PairJob:
    src_path: Path
    rip_path: Path
    flt_path: Path | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sample aligned frames from sorted src/rip/flt inputs and write plain 8-bit PNG outputs."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to the YAML config file. If omitted, local-then-system config discovery is used.",
    )
    return parser.parse_args()


def enable_windows_ansi() -> bool:
    if os.name != "nt":
        return True

    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        if handle == 0 or handle == -1:
            return False

        mode = ctypes.c_uint32()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)) == 0:
            return False

        virtual_terminal_processing = 0x0004
        if mode.value & virtual_terminal_processing:
            return True

        return kernel32.SetConsoleMode(handle, mode.value | virtual_terminal_processing) != 0
    except Exception:
        return False


def use_color_output() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if not sys.stdout.isatty():
        return False
    return enable_windows_ansi()


COLOR_ENABLED = use_color_output()


def colorize(text: str, *styles: str) -> str:
    if not COLOR_ENABLED or not styles:
        return text
    return f"{''.join(styles)}{text}{ANSI_RESET}"


def print_rule(title: str, fill: str = "=") -> None:
    body = f" {title} "
    padding = max(0, OUTPUT_WIDTH - len(body))
    left = padding // 2
    right = padding - left
    rule = f"{fill * left}{body}{fill * right}"
    print(colorize(rule, ANSI_BOLD, "\033[90m"))


def print_status(level: str, message: str) -> None:
    tag = f"[{level}]"
    tag_text = colorize(tag, ANSI_BOLD, LEVEL_STYLES.get(level, "\033[37m"))
    print(f"{tag_text} {message}")


def format_progress(current: int, total: int, width: int = 28) -> str:
    if total <= 0:
        total = 1
    current = max(0, min(current, total))
    filled = int(width * current / total)
    bar = "#" * filled + "." * (width - filled)
    percent = int(100 * current / total)
    return f"[{bar}] {current}/{total} ({percent:>3}%)"


def print_sample_progress(label: str, current: int, total: int) -> None:
    progress_label = colorize(f"{label.upper():<4}", ANSI_BOLD, "\033[34m")
    progress_bar = colorize(format_progress(current, total), "\033[96m")
    line = f"    {progress_label} {progress_bar}"
    if sys.stdout.isatty():
        print(line.ljust(OUTPUT_WIDTH), end="\n" if current >= total else "\r", flush=True)
        return

    step = max(1, total // 10)
    if current == 0 or current == total or current % step == 0:
        print(line)


def describe_job(job: PairJob) -> str:
    parts = [f"src={job.src_path.name}", f"rip={job.rip_path.name}"]
    if job.flt_path is not None:
        parts.append(f"flt={job.flt_path.name}")
    return " | ".join(parts)


def default_config_path() -> Path:
    return Path(__file__).resolve().parent / DEFAULT_CONFIG_NAME


def build_default_config_text() -> str:
    return "\n".join(
        [
            'input_dir: "."',
            "sample_itv: 5000",
            "random_seed: 19260817",
            "max_cache_size: 25600",
            "crop_param: [0, 0, 0, 0]",
            "src_prefilter: 0",
            'src_ext: ".m2ts"',
            'rip_ext: ".hevc"',
            "compare_flt: false",
            'flt_ext: ".gen.vpy"',
            'src_output_dir: "src"',
            'rip_output_dir: "rip"',
            'flt_output_dir: "flt"',
            "overwrite: false",
            "",
        ]
    )


def get_system_config_candidates() -> list[Path]:
    candidates: list[Path] = []

    if os.name == "nt":
        appdata = os.environ.get("APPDATA")
        if appdata:
            candidates.append(Path(appdata) / APP_CONFIG_DIR_NAME / DEFAULT_CONFIG_NAME)

        programdata = os.environ.get("PROGRAMDATA")
        if programdata:
            candidates.append(Path(programdata) / APP_CONFIG_DIR_NAME / DEFAULT_CONFIG_NAME)
    elif sys.platform == "darwin":
        candidates.append(Path.home() / "Library" / "Application Support" / APP_CONFIG_DIR_NAME / DEFAULT_CONFIG_NAME)
        candidates.append(Path("/Library/Application Support") / APP_CONFIG_DIR_NAME / DEFAULT_CONFIG_NAME)
    else:
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config_home:
            candidates.append(Path(xdg_config_home) / APP_CONFIG_DIR_NAME / DEFAULT_CONFIG_NAME)
        else:
            candidates.append(Path.home() / ".config" / APP_CONFIG_DIR_NAME / DEFAULT_CONFIG_NAME)

        xdg_config_dirs = os.environ.get("XDG_CONFIG_DIRS")
        if xdg_config_dirs:
            for raw_dir in xdg_config_dirs.split(os.pathsep):
                if raw_dir.strip():
                    candidates.append(Path(raw_dir) / APP_CONFIG_DIR_NAME / DEFAULT_CONFIG_NAME)
        else:
            candidates.append(Path("/etc/xdg") / APP_CONFIG_DIR_NAME / DEFAULT_CONFIG_NAME)

    unique_candidates: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        resolved_candidate = candidate.expanduser()
        if resolved_candidate in seen:
            continue
        seen.add(resolved_candidate)
        unique_candidates.append(resolved_candidate)
    return unique_candidates


def resolve_config_path(cli_config: Path | None) -> tuple[Path, str, bool]:
    if cli_config is not None:
        resolved_config = cli_config.expanduser().resolve()
        if not resolved_config.exists():
            raise FileNotFoundError(f"Explicit config file not found: {resolved_config}")
        return resolved_config, "explicit", False

    local_config = default_config_path().resolve()
    if local_config.exists():
        return local_config, "local", False

    for system_config in get_system_config_candidates():
        resolved_system_config = system_config.resolve()
        if resolved_system_config.exists():
            return resolved_system_config, "system", False

    local_config.parent.mkdir(parents=True, exist_ok=True)
    local_config.write_text(build_default_config_text(), encoding="utf-8")
    return local_config, "generated-default", True


def resolve_path(base_dir: Path, raw_value: str | os.PathLike[str]) -> Path:
    path = Path(raw_value)
    if not path.is_absolute():
        path = base_dir / path
    return path.resolve()


def normalize_suffix(raw_value: object, field_name: str) -> str:
    suffix = str(raw_value).strip()
    if not suffix:
        raise ValueError(f"{field_name} must be a non-empty file suffix.")
    if not suffix.startswith("."):
        suffix = f".{suffix}"
    return suffix.casefold()


def normalize_crop_param(raw_value: object) -> tuple[int, int, int, int]:
    if raw_value is None:
        return (0, 0, 0, 0)

    values = tuple(int(value) for value in raw_value)  # type: ignore[arg-type]
    if len(values) == 2:
        return (values[0], values[1], 0, 0)
    if len(values) == 4:
        return values

    raise ValueError("crop_param must contain either 2 values (left, right) or 4 values (left, right, top, bottom).")


def normalize_prefilter(raw_value: object) -> int:
    mapping = {
        0: 0,
        1: 1,
        2: 2,
        "0": 0,
        "1": 1,
        "2": 2,
        "none": 0,
        "ivtc": 1,
        "deinterlace": 2,
    }

    if raw_value not in mapping:
        raise ValueError("src_prefilter must be one of: 0, 1, 2, none, ivtc, deinterlace.")

    return mapping[raw_value]


def normalize_bool(raw_value: object, field_name: str) -> bool:
    if isinstance(raw_value, bool):
        return raw_value
    if isinstance(raw_value, int):
        if raw_value in (0, 1):
            return bool(raw_value)
    if isinstance(raw_value, str):
        normalized = raw_value.strip().casefold()
        if normalized in {"true", "yes", "y", "on", "1"}:
            return True
        if normalized in {"false", "no", "n", "off", "0"}:
            return False

    raise ValueError(f"{field_name} must be a boolean value.")


def load_config(config_path: Path) -> Config:
    resolved_config = config_path.resolve()
    if not resolved_config.exists():
        raise FileNotFoundError(f"Config file not found: {resolved_config}")

    raw_data = yaml.safe_load(resolved_config.read_text(encoding="utf-8")) or {}
    if not isinstance(raw_data, dict):
        raise ValueError("Config file must contain a YAML mapping at the top level.")

    base_dir = resolved_config.parent

    sample_itv = int(raw_data.get("sample_itv", 5000))
    if sample_itv <= 0:
        raise ValueError("sample_itv must be a positive integer.")

    random_seed_raw = raw_data.get("random_seed", 19260817)
    random_seed = None if random_seed_raw is None else int(random_seed_raw)

    max_cache_size = int(raw_data.get("max_cache_size", 25600))
    if max_cache_size <= 0:
        raise ValueError("max_cache_size must be a positive integer.")

    return Config(
        config_path=resolved_config,
        input_dir=resolve_path(base_dir, raw_data.get("input_dir", ".")),
        sample_itv=sample_itv,
        random_seed=random_seed,
        crop_param=normalize_crop_param(raw_data.get("crop_param", [0, 0, 0, 0])),
        src_prefilter=normalize_prefilter(raw_data.get("src_prefilter", 0)),
        src_ext=normalize_suffix(raw_data.get("src_ext", ".m2ts"), "src_ext"),
        rip_ext=normalize_suffix(raw_data.get("rip_ext", ".hevc"), "rip_ext"),
        compare_flt=normalize_bool(raw_data.get("compare_flt", False), "compare_flt"),
        flt_ext=normalize_suffix(raw_data.get("flt_ext", ".gen.vpy"), "flt_ext"),
        src_output_dir=resolve_path(base_dir, raw_data.get("src_output_dir", "src")),
        rip_output_dir=resolve_path(base_dir, raw_data.get("rip_output_dir", "rip")),
        flt_output_dir=resolve_path(base_dir, raw_data.get("flt_output_dir", "flt")),
        overwrite=normalize_bool(raw_data.get("overwrite", False), "overwrite"),
        max_cache_size=max_cache_size,
    )


def find_matching_files(directory: Path, suffix: str) -> list[Path]:
    if not directory.is_dir():
        raise FileNotFoundError(f"Input directory not found: {directory}")

    matches = [
        path.resolve()
        for path in directory.iterdir()
        if path.is_file() and path.name.casefold().endswith(suffix)
    ]
    return sorted(matches, key=lambda item: item.name.casefold())


def prepare_pairable_lists(
    config: Config,
    src_list: list[Path],
    rip_list: list[Path],
    flt_list: list[Path],
) -> tuple[list[Path], list[Path], list[Path], bool]:
    if not src_list:
        raise ValueError(f"No source files found in {config.input_dir} for {config.src_ext}.")
    if not rip_list:
        raise ValueError(f"No rip files found in {config.input_dir} for {config.rip_ext}.")
    if config.compare_flt and not flt_list:
        raise ValueError(f"No flt files found in {config.input_dir} for {config.flt_ext}.")

    lengths = [len(src_list), len(rip_list)]
    if config.compare_flt:
        lengths.append(len(flt_list))

    limit = min(lengths)
    was_truncated = len(set(lengths)) != 1

    return src_list[:limit], rip_list[:limit], flt_list[:limit], was_truncated


def build_pair_jobs(
    src_list: list[Path],
    rip_list: list[Path],
    flt_list: list[Path],
    compare_flt: bool,
) -> list[PairJob]:
    jobs: list[PairJob] = []
    for index, (src_path, rip_path) in enumerate(zip(src_list, rip_list), start=1):
        flt_path = flt_list[index - 1] if compare_flt else None
        jobs.append(PairJob(src_path=src_path, rip_path=rip_path, flt_path=flt_path))
    return jobs


def print_planned_matches(jobs: list[PairJob]) -> None:
    print_status("INFO", "planned matches after sorted-list truncation:")
    index_width = max(1, len(str(len(jobs))))

    for index, job in enumerate(jobs, start=1):
        print(f"  [{index:0{index_width}d}] {describe_job(job)}")


def print_skipped_files(label: str, skipped_files: list[Path]) -> None:
    if not skipped_files:
        return

    print_status("WARN", f"skipped {label} files due to truncation:")
    for path in skipped_files:
        print(f"  {path.name}")


def confirm_truncated_lists(
    src_list: list[Path],
    rip_list: list[Path],
    flt_list: list[Path],
    truncated_src: list[Path],
    truncated_rip: list[Path],
    truncated_flt: list[Path],
    compare_flt: bool,
) -> bool:
    print_rule("List Mismatch", "-")
    print_status("WARN", "sorted list lengths differ and will be truncated to the shortest list")
    print_status("INFO", f"src files: {len(src_list)}")
    print_status("INFO", f"rip files: {len(rip_list)}")
    if compare_flt:
        print_status("INFO", f"flt files: {len(flt_list)}")
    print_status("INFO", f"using first {len(truncated_src)} matched entries from each sorted list")

    print_planned_matches(build_pair_jobs(truncated_src, truncated_rip, truncated_flt, compare_flt))
    print_skipped_files("src", src_list[len(truncated_src):])
    print_skipped_files("rip", rip_list[len(truncated_rip):])
    if compare_flt:
        print_skipped_files("flt", flt_list[len(truncated_flt):])

    try:
        answer = input("Continue with these truncated matches? [y/N]: ").strip()
    except EOFError:
        return False
    return answer in {"Y", "y"}


def detect_rip_marker_files(rip_path: Path, rip_ext: str) -> tuple[Path, ...]:
    if rip_ext != ".hevc":
        return ()

    markers: list[Path] = []
    for marker_suffix in (".busy", ".break"):
        marker_path = rip_path.with_name(f"{rip_path.name}{marker_suffix}")
        if marker_path.exists():
            markers.append(marker_path.resolve())
    return tuple(markers)


def filter_blocked_jobs(jobs: list[PairJob], rip_ext: str) -> tuple[list[PairJob], list[tuple[PairJob, tuple[Path, ...]]]]:
    available_jobs: list[PairJob] = []
    blocked_jobs: list[tuple[PairJob, tuple[Path, ...]]] = []

    for job in jobs:
        markers = detect_rip_marker_files(job.rip_path, rip_ext)
        if markers:
            blocked_jobs.append((job, markers))
            continue
        available_jobs.append(job)

    return available_jobs, blocked_jobs


def print_blocked_jobs(blocked_jobs: list[tuple[PairJob, tuple[Path, ...]]]) -> None:
    if not blocked_jobs:
        return

    print_rule("Rip Alerts", "-")
    for job, markers in blocked_jobs:
        marker_names = ", ".join(path.name for path in markers)
        print_status("ALERT", f"rip blocked by marker file(s): {marker_names}")
        print(f"        dropped pair: {describe_job(job)}")


def apply_src_ivtc_prefilter(clip: vs.VideoNode) -> vs.VideoNode:
    return clip.tivtc.TFM().tivtc.TDecimate()


def apply_src_deinterlace_prefilter(clip: vs.VideoNode) -> vs.VideoNode:
    from havsfunc import QTGMC
    return QTGMC(clip, 'fast', TFF=True, FPSDivisor=2)


def apply_src_prefilter(clip: vs.VideoNode, mode: int) -> vs.VideoNode:
    if mode == 0:
        return clip
    if mode == 1:
        return apply_src_ivtc_prefilter(clip)
    if mode == 2:
        return apply_src_deinterlace_prefilter(clip)
    raise ValueError(f"Unsupported src prefilter mode: {mode}")


def crop_src_clip(clip: vs.VideoNode, crop_param: tuple[int, int, int, int]) -> vs.VideoNode:
    left, right, top, bottom = crop_param
    if left == 0 and right == 0 and top == 0 and bottom == 0:
        return clip
    return clip.std.Crop(left=left, right=right, top=top, bottom=bottom)


def prepare_png_clip(clip: vs.VideoNode) -> vs.VideoNode:
    return ToRGB(rks.uvsr(clip), depth=8)


def load_src_clip(src_path: Path, config: Config) -> vs.VideoNode:
    clip = rks.sourcer(str(src_path))
    clip = apply_src_prefilter(clip, config.src_prefilter)
    clip = crop_src_clip(clip, config.crop_param)
    return prepare_png_clip(clip)


def load_rip_clip(rip_path: Path) -> vs.VideoNode:
    return prepare_png_clip(rks.sourcer(str(rip_path)))


@contextmanager
def load_flt_output_clip(flt_path: Path) -> Iterator[vs.VideoNode]:
    script_path = flt_path.resolve()
    namespace = {
        "__file__": str(script_path),
        "__name__": "__vapoursynth__",
    }

    inserted_sys_path = False
    previous_cwd = Path.cwd()
    script_dir = str(script_path.parent)
    try:
        vs.clear_outputs()
        os.chdir(script_path.parent)

        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
            inserted_sys_path = True

        script_code = script_path.read_text(encoding="utf-8")
        exec(compile(script_code, str(script_path), "exec"), namespace)

        try:
            output = vs.get_output(0)
        except Exception as exc:
            raise RuntimeError(f"Failed to read output 0 from flt script: {script_path}") from exc

        if output.clip is None:
            raise RuntimeError(f"flt script did not expose a video clip on output 0: {script_path}")

        yield output.clip
    finally:
        namespace.clear()
        if inserted_sys_path:
            try:
                sys.path.remove(script_dir)
            except ValueError:
                pass
        os.chdir(previous_cwd)
        vs.clear_outputs()
        gc.collect()


@contextmanager
def load_flt_clip(flt_path: Path) -> Iterator[vs.VideoNode]:
    with load_flt_output_clip(flt_path) as clip:
        yield prepare_png_clip(clip)


def build_sample_indices(num_frames: int, sample_itv: int, rng: random.Random) -> list[int]:
    if num_frames <= 0:
        return []
    sample_count = min(math.ceil(num_frames / sample_itv), num_frames)
    return sorted(rng.sample(range(num_frames), sample_count))


def frame_width_for(num_frames: int) -> int:
    return max(1, len(str(num_frames)))


def escape_percent(value: str) -> str:
    return value.replace("%", "%%")


def build_output_template(output_dir: Path, base_name: str, label: str, frame_width: int) -> str:
    output_dir.mkdir(parents=True, exist_ok=True)
    escaped_dir = escape_percent(str(output_dir))
    escaped_base = escape_percent(base_name)
    return f"{escaped_dir}{os.sep}{escaped_base} - %0{frame_width}d - {label}.png"


def build_output_path(output_dir: Path, base_name: str, label: str, frame_width: int, frame_number: int) -> Path:
    return output_dir / f"{base_name} - {frame_number:0{frame_width}d} - {label}.png"


def write_sampled_frames(
    clip: vs.VideoNode,
    sample_indices: list[int],
    output_dir: Path,
    base_name: str,
    label: str,
    frame_width: int,
    overwrite: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_template = build_output_template(output_dir, base_name, label, frame_width)
    writer: vs.VideoNode | None = None
    total = len(sample_indices)
    written_count = 0
    skipped_existing_count = 0
    try:
        print_sample_progress(label, 0, total)
        for completed, sample_idx in enumerate(sample_indices, start=1):
            output_path = build_output_path(output_dir, base_name, label, frame_width, sample_idx)
            if not overwrite and output_path.exists():
                skipped_existing_count += 1
                print_sample_progress(label, completed, total)
                continue

            if writer is None:
                writer = clip.fpng.Write(output_template, overwrite=overwrite)

            frame = writer.get_frame(sample_idx)
            frame.close()
            written_count += 1
            print_sample_progress(label, completed, total)
    finally:
        if writer is not None:
            del writer

    if skipped_existing_count:
        print_status("INFO", f"{label}: skipped {skipped_existing_count} existing frame(s)")
    print_status("INFO", f"{label}: wrote {written_count} frame(s)")


def process_pair(
    job: PairJob,
    config: Config,
    rng: random.Random,
) -> bool:
    print_status("INFO", describe_job(job))

    src_clip = load_src_clip(job.src_path, config)
    rip_clip = load_rip_clip(job.rip_path)

    if job.flt_path is None:
        try:
            return process_clip_group(job.src_path, src_clip, rip_clip, None, config, rng)
        finally:
            del src_clip
            del rip_clip
            gc.collect()

    try:
        with load_flt_clip(job.flt_path) as flt_clip:
            return process_clip_group(job.src_path, src_clip, rip_clip, flt_clip, config, rng)
    finally:
        del src_clip
        del rip_clip
        gc.collect()


def process_clip_group(
    src_path: Path,
    src_clip: vs.VideoNode,
    rip_clip: vs.VideoNode,
    flt_clip: vs.VideoNode | None,
    config: Config,
    rng: random.Random,
) -> bool:
    frame_counts = {
        "src": src_clip.num_frames,
        "rip": rip_clip.num_frames,
    }
    if flt_clip is not None:
        frame_counts["flt"] = flt_clip.num_frames

    if len(set(frame_counts.values())) != 1:
        summary = ", ".join(f"{name}={count}" for name, count in frame_counts.items())
        print_status("SKIP", f"frame count mismatch ({summary})")
        return False

    num_frames = src_clip.num_frames
    sample_indices = build_sample_indices(num_frames, config.sample_itv, rng)
    if not sample_indices:
        print_status("SKIP", "no frames available after filtering")
        return False
    frame_width = frame_width_for(num_frames)
    base_name = src_path.stem

    print_status("INFO", f"frames: {num_frames}")
    print_status("INFO", f"samples: {len(sample_indices)}")
    print_status("INFO", f"overwrite mode: {'on' if config.overwrite else 'off'}")

    write_sampled_frames(src_clip, sample_indices, config.src_output_dir, base_name, "src", frame_width, config.overwrite)
    write_sampled_frames(rip_clip, sample_indices, config.rip_output_dir, base_name, "rip", frame_width, config.overwrite)

    if flt_clip is not None:
        write_sampled_frames(
            flt_clip,
            sample_indices,
            config.flt_output_dir,
            base_name,
            "flt",
            frame_width,
            config.overwrite,
        )

    print_status("OK", f"finished {base_name}")
    return True


def main() -> int:
    args = parse_args()
    config_path, config_source, generated_default_config = resolve_config_path(args.config)
    if generated_default_config:
        print_rule("Config Missing", "-")
        print_status("WARN", f"no config file found; created default config at {config_path}")
        print_status("WARN", "edit that config file and rerun; no comparison images were generated this time")
        return 1

    config = load_config(config_path)

    core.max_cache_size = config.max_cache_size

    full_src_list = find_matching_files(config.input_dir, config.src_ext)
    full_rip_list = find_matching_files(config.input_dir, config.rip_ext)
    full_flt_list = find_matching_files(config.input_dir, config.flt_ext) if config.compare_flt else []
    src_list, rip_list, flt_list, was_truncated = prepare_pairable_lists(
        config,
        full_src_list,
        full_rip_list,
        full_flt_list,
    )
    jobs = build_pair_jobs(src_list, rip_list, flt_list, config.compare_flt)

    print_rule("Linear Comparison V2")
    print_status("INFO", f"config: {config.config_path}")
    print_status("INFO", f"config source: {config_source}")
    print_status("INFO", f"input directory: {config.input_dir}")
    print_status("INFO", f"src files: {len(full_src_list)}")
    print_status("INFO", f"rip files: {len(full_rip_list)}")
    if config.compare_flt:
        print_status("INFO", f"flt files: {len(full_flt_list)}")
    print_status("INFO", f"sample interval: {config.sample_itv}")
    print_status("INFO", f"overwrite: {config.overwrite}")

    if was_truncated and not confirm_truncated_lists(
        full_src_list,
        full_rip_list,
        full_flt_list,
        src_list,
        rip_list,
        flt_list,
        config.compare_flt,
    ):
        print_status("STOP", "aborted: truncated match list not confirmed")
        return 1

    if was_truncated:
        print_status("INFO", f"confirmed truncated run: processing {len(jobs)} matched entries")

    jobs, blocked_jobs = filter_blocked_jobs(jobs, config.rip_ext)
    print_blocked_jobs(blocked_jobs)

    if blocked_jobs:
        print_status("WARN", f"removed {len(blocked_jobs)} blocked rip pair(s) before processing")

    if not jobs:
        print_status("STOP", "no runnable pairs remain after filtering")
        return 1

    rng = random.Random(config.random_seed)
    completed_pairs = 0

    print_rule("Processing", "-")
    for index, job in enumerate(jobs, start=1):
        print_rule(f"Pair {index}/{len(jobs)} {format_progress(index, len(jobs), width=20)}", ".")
        if process_pair(job, config, rng):
            completed_pairs += 1

    print_rule("Run Summary")
    print_status("INFO", f"scheduled pairs: {len(jobs)}")
    print_status("INFO", f"completed pairs: {completed_pairs}")
    print_status("INFO", f"skipped pairs during processing: {len(jobs) - completed_pairs}")
    if was_truncated:
        print_status("INFO", "sorted input lists were truncated to the shortest length")
    if blocked_jobs:
        print_status("INFO", f"blocked rip pairs removed: {len(blocked_jobs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
