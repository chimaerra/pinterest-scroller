import sys
from PyQt5.QtCore import QUrl, QDateTime, QEventLoop
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWebEngineCore import QWebEngineCookieStore
from PyQt5.QtNetwork import QNetworkCookie
from PyQt5.QtCore import Qt

class WebBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pinterest Webpage")
        self.setGeometry(100, 100, 800, 600)
        
        # Set window transparency to 50%
        self.setWindowOpacity(0.85)
        
        layout = QVBoxLayout()
        self.setLayout(layout)

# Request headers
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "no.pinterest.com",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "UserAgent"
}

# Request cookies
cookies = {
    "_routing_id": "\"routingid\"",
    "csrftoken": "",
    "_pinterest_sess": "==",
    "_auth": "1",
    "g_state": "{\"i_l\":0}",
    "__Secure-s_a": "==",
    "_b": "\"b=\""
}

class WebEnginePage(QWebEnginePage):
    def __init__(self, profile, *args, **kwargs):
        super(WebEnginePage, self).__init__(profile, *args, **kwargs)

    def acceptNavigationRequest(self, url, navigation_type, is_main_frame):
        if navigation_type == QWebEnginePage.NavigationTypeLinkClicked:
            return False
        return super(WebEnginePage, self).acceptNavigationRequest(url, navigation_type, is_main_frame)

class WebBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pinterest Webpage")
        self.setGeometry(100, 100, 800, 600)
        
        self.setWindowOpacity(0.15)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a QWebEngineProfile
        self.profile = QWebEngineProfile.defaultProfile()
        self.cookie_store = self.profile.cookieStore()
        self.cookie_store.deleteAllCookies()

        # Set the cookies using QWebEngineCookieStore
        for key, value in cookies.items():
            cookie = QNetworkCookie(key.encode(), value.encode())
            cookie.setDomain(".pinterest.com")
            cookie.setPath("/")
            cookie.setExpirationDate(QDateTime.currentDateTime().addYears(1))
            self.cookie_store.setCookie(cookie)

        self.web_view = QWebEngineView()
        self.web_page = WebEnginePage(self.profile, self.web_view)
        self.web_view.setPage(self.web_page)

        # Set the request headers
        self.web_page.profile().setHttpUserAgent(headers["User-Agent"])
        self.web_page.profile().setHttpAcceptLanguage(headers["Accept-Language"])
        self.web_page.profile().setHttpCacheType(QWebEngineProfile.NoCache)
        self.web_page.profile().setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)

        # Disable the InstalledAppProvider interface
        self.web_view.settings().setAttribute(QWebEngineSettings.AutoLoadIconsForPage, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)

        layout.addWidget(self.web_view)

        self.load_webpage()

    def load_webpage(self):
        url = QUrl("https://no.pinterest.com/")
        self.web_view.loadFinished.connect(self.on_load_finished)
        self.web_view.load(url)

    def on_load_finished(self, ok):
        if ok:
            self.web_view.page().runJavaScript("""
                function removeUnwantedElements() {
                    var headerElement = document.querySelector('div[data-test-id="header"]#HeaderContent');
                    if (headerElement) {
                        headerElement.remove();
                    }
                    
                    var footerElement = document.querySelector('div.footerButtons');
                    if (footerElement) {
                        footerElement.remove();
                    }
                    
                    setTimeout(removeUnwantedElements, 10);
                }
                
                removeUnwantedElements();
                
                // Change the background color of the webpage
                document.body.style.backgroundColor = '#38383b';
                // Polyfill for replaceAll() function
                if (!String.prototype.replaceAll) {
                    String.prototype.replaceAll = function(search, replace) {
                        return this.split(search).join(replace);
                    };
                }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv + ['--disable-features=InstalledApp'])
    browser = WebBrowser()
    browser.show()
    sys.exit(app.exec_())