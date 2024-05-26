$(function() {
    function EnvironmentDataViewModel(parameters) {
        var self = this;

        self.htmlContent = ko.observable("");
        self.error = ko.observable("");

        // Receive data from backend
        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin !== "environment_data_grabber") {
                return;
            }

            if (data.error) {
                self.error(data.error);
                self.htmlContent("");
            } else {
                self.error("");
                self.htmlContent(data.html_content);
            }
        };
    }

    // Register the view model
    OCTOPRINT_VIEWMODELS.push({
        construct: EnvironmentDataViewModel,
        dependencies: [],
        elements: ["#environment_data_grabber_plugin"]
    });
});
