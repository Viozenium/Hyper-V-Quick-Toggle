import pytest

tk = pytest.importorskip("tkinter")

from hyperv_toggle import ui as ui_module
from hyperv_toggle.constants import (
    ACCENT_GREEN,
    ACCENT_ORA,
    ACCENT_RED,
    STATO_OFF,
    STATO_ON,
)


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setattr(ui_module, "get_hyperv_state", lambda: STATO_OFF)
    try:
        instance = ui_module.HyperVApp()
    except tk.TclError as exc:
        pytest.skip(f"Tkinter non disponibile in questo ambiente: {exc}")
    yield instance
    instance.destroy()


def test_on_status_read_auto_enables_off_button(app):
    app._on_status_read(STATO_ON, None)
    assert "disabled" in app.btn_on.state()
    assert "disabled" not in app.btn_off.state()
    assert str(app.status_label.cget("foreground")) == ACCENT_GREEN


def test_on_status_read_off_enables_on_button(app):
    app._on_status_read(STATO_OFF, None)
    assert "disabled" in app.btn_off.state()
    assert "disabled" not in app.btn_on.state()
    assert str(app.status_label.cget("foreground")) == ACCENT_ORA


def test_on_status_read_error_shows_error_state(app, monkeypatch):
    monkeypatch.setattr(ui_module.messagebox, "showerror", lambda *a, **k: None)
    app._on_status_read(None, "boom")
    assert str(app.status_label.cget("foreground")) == ACCENT_RED


def test_on_status_read_unknown_state_shows_error_color(app):
    app._on_status_read(None, None)
    assert str(app.status_label.cget("foreground")) == ACCENT_RED


def test_set_busy_true_disables_all_buttons(app):
    app._set_busy(True)
    for btn in (app.btn_on, app.btn_off, app.btn_refresh, app.btn_reboot):
        assert "disabled" in btn.state()


def test_set_busy_false_reenables_refresh_and_reboot(app):
    app._set_busy(True)
    app._set_busy(False)
    assert "disabled" not in app.btn_refresh.state()
    assert "disabled" not in app.btn_reboot.state()
