import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor, QPalette, QKeySequence, QIcon, QPixmap, QTransform, QFont, QAction, QShortcut
from PyQt6.QtWebEngineWidgets import QWebEngineView
import re
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineProfile
from PyQt6.QtCore import QUrl

# NOTES / TO-DO: 
# Adblock score: 51 points out of 100
# Maybe add extra stuff in search overlay?

class adblock(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        url = info.requestUrl()
        if self.is_ad_url(url):
            info.block(True)
        else:
            info.block(False)

    def is_ad_url(self, url: QUrl) -> bool:
        ad_domains = [
            "doubleclick.net",
            "adservice.google.com",
            "ads.yahoo.com",
            "pagead2.googlesyndication.com",
            "advertising.com",
            "adclick.g.doubleclick.net",
            "adnxs.com",
            "adsrvr.org",
            "pubmatic.com",
            "openx.net",
            "rubiconproject.com",
            "criteo.com",
            "adroll.com",
            "mediaplex.com",
            "yieldmanager.com",
            "googleadservices.com",
            "appnexus.com",
            "outbrain.com",
            "taboola.com",
            "brightcove.com",
            "revcontent.com",
            "spotxchange.com",
            "sharethrough.com",
            "adblade.com",
            "exponential.com",
            "indexexchange.com",
            "bidswitch.net",
            "gumgum.com",
            "ads-twitter.com",
            "contextweb.com",
            "bidvertiser.com",
            "chitika.net",
            "conversantmedia.com",
            "adform.net",
            "rocketfuel.com",
            "tribalfusion.com",
            "media.net",
            "smaato.net",
            "adf.ly",
            "propellerads.com",
            "popads.net",
            "adsterra.com",
            "mgid.com",
            "zedo.com",
            "innity.com",
            "clicksor.com",
            "trafficjunky.net",
            "plista.com",
            "vungle.com",
            "unityads.unity3d.com",
            "adsense.google.com",
            "moat.com",
            "quantserve.com",
            "skimlinks.com",
            "viglink.com",
            "tradedoubler.com",
            "cj.com",
            "impact.com", 
            "clickbank.net"
        ]
        return any(domain in url.host() for domain in ad_domains)


colorScheme = {
    "base": QColor(30, 30, 46),
    "text": QColor(255, 255, 255),
    "accent": QColor(35, 160, 172),
    "background": QColor(49, 50, 68),
    "button": QColor(24, 24, 37),
    "hover": QColor(17, 17, 27),
}

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.adblockthing = adblock()
        
        profile = QWebEngineProfile.defaultProfile()
        profile.setUrlRequestInterceptor(self.adblockthing)


        self.setWindowTitle("WebTree")
        self.setGeometry(100, 100, 1200, 800)
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.newTab()

        self.tabs.currentChanged.connect(self.changecheck)

        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: #45475a;
                color: white;
                margin: 3px 5px 3px 10px;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid #45475a;
                margin-top: 10px;
                font-family: 'Poppins', sans-serif;
                font-size: 14px;
            }
            QTabBar::tab:hover {
                background: rgb(49, 50, 68);
            }
            QTabBar::tab:selected {
                background: rgb(49, 50, 68);
                border: 2px solid #eba0ac;
                color: #eba0ac;
            }

            QTabWidget::pane {
                border-radius: 10px;
                padding: 10px;
                padding-top: 10px;
            }
        """)

        self.tabs.setMovable(True)

        navbar = self.makenav()
        self.addToolBar(navbar)

        self.shortset()

        self.create_searchy()

        self.mtb()
        navbar.setMovable(False)


        self.progress = QProgressBar(self)
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setGeometry(0, 45, self.width(), 3)
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: #eba0ac;
                border-radius: 0px;
            }
            QProgressBar::chunk {
                background-color: #eba0ac;
                border-radius: 0px;
            }
        """)
        self.progress.setVisible(False)

    def makenav(self):
        navbar = QToolBar()
        navbar.setStyleSheet("""
            QToolBar {
                background-color: rgb(30, 30, 46);
                font-family: 'Poppins', sans-serif;
            }
            QToolBar QToolButton {
                color: rgb(255, 255, 255);
                font-size: 17px;
                background: #45475a;
                margin: 8px 15px;
                border-radius: 5px;
                font-family: 'Mononoki Nerd Font Mono Regular';
                padding-top: 5px;
                padding-bottom: 5px;
            }
            QToolBar QToolButton:hover {
                color: rgb(255, 255, 255);
                background: #eba0ac;
                color: #45475a;
            }
            QLineEdit {
                background-color: #45475a;
                color: #9399b2;
                padding: 5px 10px;
                font-size: 16px;
                font-family: 'Poppins', sans-serif;
                text-align: left;
                border: 2px solid #45475a;     
                border-radius: 17px;     
                margin-top: 5px;
                margin-bottom: 5px;
            }
            QLineEdit:focus {
                color: white;   
                border: 2px solid #eba0ac;          
            }
        """)        
        self.buttons(navbar)
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.goto)
        navbar.addWidget(self.url_bar)
        navbar.setIconSize(QSize(10, 10))
        return navbar
    
    def goto(self):
        url = self.url_bar.text()
        if self.httquestion(url):
            url = self.httpify(url)
        else:
            url = f"https://www.google.com/search?q={url}"
        self.tabs.currentWidget().setUrl(QUrl(url))

    def buttons(self, navbar):
        buttons = [
            ("go-previous", '  ', self.back),
            ("go-next", '  ', self.forward),
            ("view-refresh", '  ', self.reload),
            ("tab-new", '  ', self.newTab),
            ("window-close", '  ', self.closet)
        ]
        for icon, label, action in buttons:
            btn = QAction(label, self)
            btn.triggered.connect(action)
            navbar.addAction(btn)

    def shortset(self):
        shortcuts = {
            "Ctrl+Space": self.open_searchy,
            "Ctrl+T": self.newTab,
            "Ctrl+W": self.closet,
            "Ctrl+R": self.reload,
            "Alt+Left": self.back,
            "Alt+Right": self.forward,
            "Ctrl+Q": self.close,
            "Ctrl+Left": self.moveback,
            "Ctrl+Right": self.movef,
            "Ctrl+Down": self.moveback,
            "Ctrl+Up": self.movef,
        }
        
        for key, func in shortcuts.items():
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(func)
    
    def changecheck(self, index):
        current_browser = self.tabs.widget(index)
        if isinstance(current_browser, QWebEngineView):
            self.url_bar.setText(current_browser.url().toString())
            self.url_bar.setCursorPosition(0)

    def moveback(self):
        current_index = self.tabs.currentIndex()
        if current_index > 0:
            self.tabs.setCurrentIndex(current_index - 1)

    def movef(self):
        current_index = self.tabs.currentIndex()
        if current_index < self.tabs.count() - 1:
            self.tabs.setCurrentIndex(current_index + 1)


    def create_searchy(self):
        self.searchy = QWidget(self)
        self.searchy.setStyleSheet(f"""
            background-color: {colorScheme['base'].name()};
            border-radius: 15px;
            border: 2px solid #7E6F66;
            font-family: 'Poppins', sans-serif;
            padding-left: 20px;
        """)
        self.searchy.setVisible(False)

        overlayW = 600
        overlayH = 120
        self.searchy.setFixedSize(overlayW, overlayH)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 50))  
        shadow.setOffset(0, 4)
        self.searchy.setGraphicsEffect(shadow)

        self.search_layout = QHBoxLayout(self.searchy)
        self.search_layout.setContentsMargins(20, 20, 20, 20)
        self.search_layout.setSpacing(10)

        self.search_input = QLineEdit(self.searchy)
        self.suggestions_widget = QWidget(self.searchy)
        self.suggestions_layout = QVBoxLayout(self.suggestions_widget)
        self.suggestions_layout.setContentsMargins(0, 0, 0, 0)
        self.suggestions_layout.setSpacing(5)
        self.search_layout.addWidget(self.suggestions_widget)
        self.search_input.setStyleSheet(f"""
            background-color: {colorScheme['button'].name()};
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
            color: {colorScheme['text'].name()};
            border: none;
        """)
        self.search_input.setPlaceholderText("Type your search...")
        self.search_input.returnPressed.connect(self.search)

        self.search_layout.addWidget(self.search_input)

        self.shortcut_close_search = QShortcut(QKeySequence("Esc"), self)
        self.shortcut_close_search.activated.connect(self.close_searchy)

        self.centerOvr()

    def centerOvr(self):
        window_geometry = self.geometry()
        overlayW = self.searchy.width()
        overlayH = self.searchy.height()

        center_x = (window_geometry.width() - overlayW) // 2
        center_y = (window_geometry.height() - overlayH) // 2

        self.searchy.move(center_x, center_y)

    def textChange(self):
        if self.search_input.text(): 
            self.bounce.stop()  
            self.bounce.start()

    def open_searchy(self):
        self.searchy.setVisible(True)
        self.search_input.clear()
        self.search_input.setFocus()
        self.searchy.setStyleSheet(f"border-color: #f38ba8;")
        self.search_input.setStyleSheet(f"background-color: {colorScheme['button'].name()};"
                                        f"border-radius: 10px; padding: 10px; font-size: 18px; "
                                        f"border-color: #f38ba8; "
                                        f"color: {colorScheme['text'].name()};")
        self.animate_searchy()

    def animate_searchy(self):
        overlayW, overlayH = 600, 120
        window_width, window_height = self.width(), self.height()

        x_pos, y_pos = (window_width - overlayW) // 2, (window_height - overlayH) // 2

        self.animation = QPropertyAnimation(self.searchy, b"geometry")
        self.animation.setDuration(300)
        self.animation.setStartValue(QRect(x_pos, window_height, overlayW, overlayH))
        self.animation.setEndValue(QRect(x_pos, y_pos, overlayW, overlayH))
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()

    def close_searchy(self):
        self.animation = QPropertyAnimation(self.searchy, b"geometry")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.searchy.geometry())
        self.animation.setEndValue(QRect(self.searchy.x(), self.height(), 
                                        self.searchy.width(), self.searchy.height()))
        self.animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.animation.finished.connect(lambda: self.searchy.setVisible(False))
        self.animation.start()

    def search(self):
        query = self.search_input.text()
        if query:
            if self.httquestion(query):
                url = self.httpify(query)
            else:
                url = f"https://www.google.com/search?q={query}"
            self.tabs.currentWidget().setUrl(QUrl(url))
        self.close_searchy()

    def httquestion(self, url):
        return re.match(r'^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}', url) is not None

    def httpify(self, url):
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        return url

    def newTab(self):
        newtabhtml = """
            <html>
            <head>
                <title>New Tab</title>
                <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
                <style>
                    body {
                        background-color: #1e1e2e;
                        color: #bac2de;
                        font-family: 'Poppins', sans-serif;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        text-align: center;
                    }
                    h1 {
                        font-size: 50px;
                        color: #f38ba8;
                        font-weight: 600;
                        margin-bottom: 20px;
                    }
                    h1 span {
                        display: inline-block;
                        transition: transform 0.3s ease, color 0.3s ease;
                    }
                    h1 span:hover {
                        transform: translateY(-10px);
                        color: #89dceb;
                    }
                    input[type="text"] {
                        width: 60%;
                        padding: 12px;
                        border: none;
                        border-radius: 10px;
                        font-size: 18px;
                        font-family: 'Poppins', sans-serif;
                        background-color: #313244;
                        border: 2px solid #313244;
                        color: white;
                        margin-top: 20px;
                    }
                    input[type="text"]:focus {
                        outline: none;
                        border: 2px solid #AA8BDC;
                    }
                </style>
            </head>
            <body>
                <h1>
                    <span>W</span><span>e</span><span>b</span><span>T</span><span>r</span><span>e</span><span>e</span>
                </h1>
                <input type="text" id="search_bar" placeholder="🔍 Search the web. (Ctrl + Space or Click)" />
                <script>
                    document.getElementById('search_bar').addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') {
                            let query = document.getElementById('search_bar').value;
                            window.location.href = 'https://www.google.com/search?q=' + encodeURIComponent(query);
                        }
                    });
                </script>
            </body>
            </html>
        """
        browser = QWebEngineView()
        browser.setHtml(newtabhtml)
        browser.urlChanged.connect(self.updatebar)
        browser.urlChanged.connect(lambda url: self.tabn(browser))
        browser.loadStarted.connect(self.showp)
        browser.loadFinished.connect(self.hprog)
        browser.page().iconChanged.connect(lambda: self.tabn(browser))
        browser.page().titleChanged.connect(lambda: self.tabn(browser))        
        self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentWidget(browser)

    def updatebar(self, url):
        self.url_bar.setText(url.toString())
        self.url_bar.setCursorPosition(0)
        
    def favifavi(self, browser):
        page = browser.page()
        page.iconChanged.connect(lambda icon: self.tabn(browser))

    def tabn(self, browser, ml=20):
        index = self.tabs.indexOf(browser)
        if index != -1:
            page_title = browser.page().title()
            page_icon = browser.page().icon()
            
            if len(page_title) > ml:
                page_title = page_title[:ml] + "..."
            
            self.tabs.setTabIcon(index, page_icon)
            self.tabs.setTabText(index, page_title if page_title else "Loading...")

    def closet(self):
        current_tab = self.tabs.currentWidget()
        current_tab.deleteLater()
        self.tabs.removeTab(self.tabs.indexOf(current_tab))

    def back(self):
        self.tabs.currentWidget().back()

    def forward(self):
        self.tabs.currentWidget().forward()

    def reload(self):
        self.tabs.currentWidget().reload()

    def mtb(self):
        self.plus_button = QPushButton('+', self)
        self.plus_button.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        self.plus_button.setStyleSheet('''
            QPushButton {
                background-color: #45475a;
                color: white;
                border-radius: 5px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #3a3e47;
            }
            QPushButton:pressed {
                background-color: #6a6e77;
            }
        ''')
        self.plus_button.setFixedSize(30, 30)
        self.plus_button.clicked.connect(self.newTab)

        self.buttonpos()
        self.plus_button.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.buttonpos()
        self.centerOvr()
    
    def centerOvr(self):
        overlayW, overlayH = self.searchy.width(), self.searchy.height()
        window_width, window_height = self.width(), self.height()

        x_pos = (window_width - overlayW) // 2
        y_pos = (window_height - overlayH) // 2

        self.searchy.move(x_pos, y_pos)


    def buttonpos(self):
        if hasattr(self, 'plus_button'):
            button_width = self.plus_button.width()
            self.plus_button.move(self.width() - button_width - 10, 60)

    def showp(self):
        self.progress.setVisible(True)
        self.progress.setValue(0)

    def hprog(self, ok):
        self.progress.setVisible(False)
        self.progress.setValue(100)

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("WebTree")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, colorScheme["base"])
    palette.setColor(QPalette.ColorRole.Text, colorScheme["text"])  # Fixed here
    app.setPalette(palette)
    
    window = Browser()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
