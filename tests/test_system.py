import subprocess

import pytest

from hyperv_toggle import system
from hyperv_toggle.constants import STATO_OFF, STATO_ON

# ----------------------
# get_hyperv_state


def test_get_hyperv_state_returns_auto(monkeypatch):
    monkeypatch.setattr(
        system,
        "run_command",
        lambda cmd: "hypervisorlaunchtype    Auto\nother line   value",
    )
    assert system.get_hyperv_state() == STATO_ON


def test_get_hyperv_state_returns_off(monkeypatch):
    monkeypatch.setattr(
        system, "run_command", lambda cmd: "hypervisorlaunchtype    Off"
    )
    assert system.get_hyperv_state() == STATO_OFF


def test_get_hyperv_state_returns_none_when_not_present(monkeypatch):
    monkeypatch.setattr(
        system,
        "run_command",
        lambda cmd: "some other bcdedit output\nwithout the key",
    )
    assert system.get_hyperv_state() is None


# ----------------------
# run_command


def test_run_command_returns_stripped_stdout(monkeypatch):
    class FakeResult:
        stdout = "  output value  \n"

    def fake_run(cmd_list, **kwargs):
        assert kwargs["check"] is True
        return FakeResult()

    monkeypatch.setattr(system.subprocess, "run", fake_run)
    assert system.run_command(["echo", "hi"]) == "output value"


def test_run_command_raises_runtime_error_with_stderr(monkeypatch):
    def fake_run(cmd_list, **kwargs):
        raise subprocess.CalledProcessError(1, cmd_list, stderr="dettaglio errore")

    monkeypatch.setattr(system.subprocess, "run", fake_run)
    with pytest.raises(RuntimeError, match="dettaglio errore"):
        system.run_command(["bcdedit"])


def test_run_command_raises_runtime_error_without_stderr(monkeypatch):
    def fake_run(cmd_list, **kwargs):
        raise subprocess.CalledProcessError(1, cmd_list, stderr="")

    monkeypatch.setattr(system.subprocess, "run", fake_run)
    with pytest.raises(RuntimeError, match="Comando fallito"):
        system.run_command(["bcdedit"])


def test_run_command_raises_runtime_error_on_missing_executable(monkeypatch):
    def fake_run(cmd_list, **kwargs):
        raise FileNotFoundError()

    monkeypatch.setattr(system.subprocess, "run", fake_run)
    with pytest.raises(RuntimeError, match="Comando non trovato: bcdedit"):
        system.run_command(["bcdedit"])


# ----------------------
# is_admin


def test_is_admin_true(monkeypatch):
    monkeypatch.setattr(system.ctypes.windll.shell32, "IsUserAnAdmin", lambda: 1)
    assert system.is_admin() is True


def test_is_admin_false_on_exception(monkeypatch):
    def raise_exc():
        raise OSError("no admin info")

    monkeypatch.setattr(system.ctypes.windll.shell32, "IsUserAnAdmin", raise_exc)
    assert system.is_admin() is False


# ----------------------
# elevate_and_relaunch


def test_elevate_and_relaunch_uses_script_directory(monkeypatch, tmp_path):
    captured = {}

    def fake_shell_execute(hwnd, verb, file, params, directory, show):
        captured["directory"] = directory
        return 42  # > 32 -> avviato con successo

    monkeypatch.setattr(
        system.ctypes.windll.shell32, "ShellExecuteW", fake_shell_execute
    )
    monkeypatch.setattr(system.sys, "argv", [str(tmp_path / "Hyper-V.py")])

    assert system.elevate_and_relaunch() is True
    assert captured["directory"] == str(tmp_path)


def test_elevate_and_relaunch_false_when_declined(monkeypatch, tmp_path):
    monkeypatch.setattr(system.ctypes.windll.shell32, "ShellExecuteW", lambda *a: 5)
    monkeypatch.setattr(system.sys, "argv", [str(tmp_path / "Hyper-V.py")])
    assert system.elevate_and_relaunch() is False


def test_elevate_and_relaunch_false_on_exception(monkeypatch, tmp_path):
    def raise_exc(*a):
        raise OSError("boom")

    monkeypatch.setattr(system.ctypes.windll.shell32, "ShellExecuteW", raise_exc)
    monkeypatch.setattr(system.sys, "argv", [str(tmp_path / "Hyper-V.py")])
    assert system.elevate_and_relaunch() is False
