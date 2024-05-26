/*
 * View model for environment_data_grabber
 *
 * Author: Jan Feddern
 * License: AGPLv3
 */
$(function() {
    function EnvironmentDataViewModel(parameters) {
        var self = this;

        self.luftfeuchtigkeit = ko.observable();
        self.temperatur = ko.observable();

        // Receive data from backend
        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin !== "environment_data_grabber") {
                return;
            }

            if (data.luftfeuchtigkeit) {
                self.luftfeuchtigkeit(data.luftfeuchtigkeit);
            }
            if (data.temperatur) {
                self.temperatur(data.temperatur);
            }
        };
    }

    // Register the view model
    OCTOPRINT_VIEWMODELS.push({
        construct: EnvironmentDataViewModel,
        dependencies: [],
        elements: ["#navbar_plugin_environment_data_grabber"]
    });
});
