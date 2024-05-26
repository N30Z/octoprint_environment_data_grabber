import octoprint.plugin
import requests
from bs4 import BeautifulSoup

class EnvironmentDataGrabberPlugin(octoprint.plugin.StartupPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.AssetPlugin):

    def on_startup(self, host, port):
        self._logger.info("Environment Data Grabber Plugin started")
        self.fetch_data()

    def fetch_data(self):
        url = "http://192.168.178.57/"  # Replace with the actual IP address and endpoint
        try:
            response = requests.get(url)
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract humidity and temperature
            luftfeuchtigkeit_element = soup.find(text="Luftfeuchtigkeit:")
            temperatur_element = soup.find(text="Temperatur:")

            if luftfeuchtigkeit_element and temperatur_element:
                luftfeuchtigkeit = luftfeuchtigkeit_element.find_next().text
                temperatur = temperatur_element.find_next().text

                self._logger.info(f"Luftfeuchtigkeit: {luftfeuchtigkeit}")
                self._logger.info(f"Temperatur: {temperatur}")

                # Send data to frontend
                self._plugin_manager.send_plugin_message(self._identifier, dict(luftfeuchtigkeit=luftfeuchtigkeit, temperatur=temperatur))
            else:
                self._logger.error("Failed to find the required elements in the HTML.")
                self._plugin_manager.send_plugin_message(self._identifier, dict(error="Failed to find the required elements in the HTML."))

        except requests.RequestException as e:
            self._logger.error(f"Error fetching data: {e}")
            self._plugin_manager.send_plugin_message(self._identifier, dict(error="Error fetching data: Unable to reach the website."))

    def get_template_configs(self):
        return [dict(type="navbar", custom_bindings=True)]

    def get_assets(self):
        return dict(js=["js/environment_data_grabber.js"],
                    css=["css/environment_data_grabber.css"])

__plugin_name__ = "Environment Data Grabber"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = EnvironmentDataGrabberPlugin()
