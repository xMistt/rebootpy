
$(document).ready(function() {
    const settingsBackground = $("#settings-background");
    const settingsContainer = $("#settings-container");
    const settingsButton = $("#settings-button");
    const settingsCloseButton = $("#settings-close-button");

    const themeRadioLight = $("#radio-theme-light");
    const themeRadioDark = $("#radio-theme-dark");
    const lightLabel = $("#radio-label-theme-light");
    const darkLabel = $("#radio-label-theme-dark");

    const isSettingsVisible = () => settingsBackground.css("display") === "flex";

    const toggleSettingsVisibility = (visible = !isSettingsVisible()) => {
        settingsBackground.css("display", visible ? "flex" : "none");
    };

    settingsButton.on('click', toggleSettingsVisibility);
    settingsBackground.on('click', toggleSettingsVisibility);

    settingsContainer.on('click', (e) => {
        e.stopPropagation();
    });

    settingsCloseButton.on('click', toggleSettingsVisibility);

    // Settings actions
    lightLabel.on('click', () => {
        setTheme("light");
    });

    darkLabel.on('click', () => {
        setTheme("dark");
    });

    const currentThemeRadio = getCurrentTheme() === "light" ? themeRadioLight : themeRadioDark;
    currentThemeRadio.attr("checked", "checked");
});
