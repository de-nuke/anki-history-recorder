from PyQt5 import QtWidgets
from anki.cards import Card
from anki.hooks import wrap
from aqt.reviewer import Reviewer, ReviewerBottomBar
from aqt import gui_hooks, mw, qconnect
from aqt.webview import WebContent

from .contrib import open_files_folder, show_files_choice_window, \
    open_upload_page
from .session import session


mw.addonManager.setWebExports(__name__, r"web/.*(css|js)")


def did_answer_card(reviewer, card, ease):
    session.save_answer(reviewer, card, ease)


def did_show_answer(card):
    session.save_answer_shown(card)


def card_will_show(text: str, card: Card, kind: str) -> str:
    return session.before_card_show(text, card, kind)


def start_session(self):
    session.start()


def stop_session():
    session.stop()


def switch_addon_on_off(action_widget):
    def _switch():
        session.toggle_on_off()
        if session.enabled is True:
            action_widget.setText("Turn off")
            enabled = "true"
        else:
            action_widget.setText("Turn on")
            enabled = "false"

        mw.reviewer.bottom.web.eval(f"setRecorderEnabled({enabled})")
    return _switch


def add_menu_actions():
    open_dir_action = QtWidgets.QAction(mw)
    submit_history_action = QtWidgets.QAction(mw)
    open_browser_action = QtWidgets.QAction(mw)
    on_off_action = QtWidgets.QAction(mw)
    open_dir_action.setText("Open files folder")
    open_browser_action.setText("Open upload form in browser")
    submit_history_action.setText("Submit history...")
    on_off_action.setText("Turn off")
    submenu = mw.form.menuTools.addMenu("History recorder")
    submenu.addAction(on_off_action)
    submenu.addAction(open_dir_action)
    submenu.addAction(open_browser_action)
    submenu.addAction(submit_history_action)
    qconnect(open_dir_action.triggered, open_files_folder)
    qconnect(submit_history_action.triggered, show_files_choice_window)
    qconnect(open_browser_action.triggered, open_upload_page)
    qconnect(on_off_action.triggered, switch_addon_on_off(on_off_action))

    return {
        "open_dir": open_dir_action,
        "submit_history": submit_history_action,
        "open_browser": open_browser_action,
        "on_off": on_off_action
    }


def will_set_content(web_content: WebContent, context):
    if isinstance(context, ReviewerBottomBar):
        addon_package = mw.addonManager.addonFromModule(__name__)
        web_content.js.append(f"/_addons/{addon_package}/web/script.js")
        web_content.css.append(f"/_addons/{addon_package}/web/style.css")

        html_template = """
        <div id="history-recorder-status">
            <span class="text {on_off_class}">{label}</span>
            <label class="history-recorder-switch">
                <input type="checkbox" {checked} id="history-recorder-checkbox">
                <span class="slider round"></span>
            </label>
        </div>
        """

        web_content.body += html_template.format(
            checked="checked" if session.enabled else "",
            label="Your answers are being recorded"
            if session.enabled else "Answer recording is stopped",
            on_off_class="on" if session.enabled else "off"
        )


def webview_did_receive_js_message(action_widget):
    def _webhook_did_receive_js_message(handled, message, context):
        if message.startswith("recorder_status_changed"):
            enabled = message.rsplit(";", 1)[1]
            if enabled == "true":
                session.enabled = True
                action_widget.setText("Turn off")
            elif enabled == "false":
                session.enabled = False
                action_widget.setText("Turn on")
            return True, None
        return handled
    return _webhook_did_receive_js_message


actions = add_menu_actions()

Reviewer.show = wrap(Reviewer.show, start_session)
gui_hooks.reviewer_will_end.append(stop_session)
gui_hooks.reviewer_did_answer_card.append(did_answer_card)
gui_hooks.card_will_show.append(card_will_show)
gui_hooks.reviewer_did_show_answer.append(did_show_answer)
gui_hooks.webview_will_set_content.append(will_set_content)
gui_hooks.webview_did_receive_js_message.append(
    webview_did_receive_js_message(actions["on_off"])
)
