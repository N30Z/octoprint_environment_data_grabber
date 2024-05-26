import octoprint.plugin
import requests

class EnvironmentDataGrabberPlugin(octoprint.plugin.StartupPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.AssetPlugin):

    def on_startup(self, host, port):
        self._logger.info("Environment Data Grabber Plugin started")
        self.fetch_data()

    def fetch_data(self):
        url = "http://192.168.1.100"  # Replace with the actual IP address
        try:
            self._logger.info("Fetching data from the specified URL...")
            response = requests.get(url)
            response.raise_for_status()
            html_content = response.text

            # Send data to frontend
            self._plugin_manager.send_plugin_message(self._identifier, dict(html_content=html_content))
            self._logger.info("Data fetched successfully.")

        except requests.RequestException as e:
            self._logger.error(f"Error fetching data: {e}")
            self._plugin_manager.send_plugin_message(self._identifier, dict(error="Error fetching data: Unable to reach the website."))

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=True),
            dict(type="navbar", custom_bindings=True),
            dict(type="tab", name="Environment Data", custom_bindings=True),
        ]

    def get_assets(self):
        return dict(js=["js/environment_data_grabber.js"],
                    css=["css/environment_data_grabber.css"])

__plugin_name__ = "Environment Data Grabber"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = EnvironmentDataGrabberPlugin()
