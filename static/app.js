"use strict";

const dashboard = {
    async fetchJSON(url) {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            },
            cache: "no-store"
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        return await response.json();
    },

    async load() {
        const healthIndicator =
            document.getElementById("healthIndicator");

        const healthIcon =
            document.getElementById("healthIcon");

        const healthStatus =
            document.getElementById("healthStatus");

        const healthMessage =
            document.getElementById("healthMessage");

        try {
            const [health, status, info] = await Promise.all([
                this.fetchJSON("/health"),
                this.fetchJSON("/api/status"),
                this.fetchJSON("/api/info")
            ]);

            this.updateHealth(health);
            this.updateStatus(status);
            this.updateInfo(info);

            const apiResponse =
                document.getElementById("apiResponse");

            if (apiResponse) {
                apiResponse.textContent =
                    JSON.stringify(
                        {
                            health,
                            status,
                            info
                        },
                        null,
                        2
                    );
            }

            const lastUpdated =
                document.getElementById("lastUpdated");

            if (lastUpdated) {
                lastUpdated.textContent =
                    `Updated ${new Date().toLocaleTimeString()}`;
            }

        } catch (error) {

            console.error(
                "Dashboard API error:",
                error
            );

            if (healthIndicator) {
                healthIndicator.textContent = "Offline";
                healthIndicator.className =
                    "health-indicator offline";
            }

            if (healthIcon) {
                healthIcon.textContent = "!";
                healthIcon.className =
                    "health-icon offline";
            }

            if (healthStatus) {
                healthStatus.textContent =
                    "Server unavailable";
            }

            if (healthMessage) {
                healthMessage.textContent =
                    "Could not connect to the Python API";
            }

            const apiResponse =
                document.getElementById("apiResponse");

            if (apiResponse) {
                apiResponse.textContent =
                    JSON.stringify(
                        {
                            status: "error",
                            message:
                                "Backend API unavailable"
                        },
                        null,
                        2
                    );
            }
        }
    },

    updateHealth(data) {

        const indicator =
            document.getElementById("healthIndicator");

        const icon =
            document.getElementById("healthIcon");

        const status =
            document.getElementById("healthStatus");

        const message =
            document.getElementById("healthMessage");

        const isOnline =
            data &&
            (
                data.status === "ok" ||
                data.status === "healthy" ||
                data.status === "online"
            );

        if (indicator) {
            indicator.textContent =
                isOnline ? "Online" : "Offline";

            indicator.className =
                isOnline
                    ? "health-indicator online"
                    : "health-indicator offline";
        }

        if (icon) {
            icon.textContent =
                isOnline ? "✓" : "!";

            icon.className =
                isOnline
                    ? "health-icon online"
                    : "health-icon offline";
        }

        if (status) {
            status.textContent =
                isOnline
                    ? "System operational"
                    : "System unavailable";
        }

        if (message) {
            message.textContent =
                isOnline
                    ? "Python backend is responding normally"
                    : "Backend health check failed";
        }
    },

    updateStatus(data) {

        const service =
            document.getElementById("serviceName");

        const status =
            document.getElementById("serverStatus");

        const version =
            document.getElementById("serverVersion");

        const port =
            document.getElementById("serverPort");

        if (service) {
            service.textContent =
                data.service || "Unknown";
        }

        if (status) {
            status.textContent =
                data.status || "Unknown";
        }

        if (version) {
            version.textContent =
                data.version || "Unknown";
        }

        if (port) {
            port.textContent =
                data.port || "Unknown";
        }

        this.updateUptime(
            data.uptime_seconds
        );
    },

    updateInfo(data) {

        const python =
            document.getElementById("pythonVersion");

        const platform =
            document.getElementById("platformInfo");

        const architecture =
            document.getElementById(
                "architectureInfo"
            );

        const environment =
            document.getElementById(
                "environmentInfo"
            );

        if (python) {
            python.textContent =
                data.python_version || "Unknown";
        }

        if (platform) {
            platform.textContent =
                data.platform || "Unknown";
        }

        if (architecture) {
            architecture.textContent =
                data.architecture || "Unknown";
        }

        if (environment) {
            environment.textContent =
                data.environment || "Unknown";
        }
    },

    updateUptime(seconds) {

        const uptime =
            document.getElementById(
                "uptimeValue"
            );

        const progress =
            document.getElementById(
                "uptimeProgress"
            );

        if (
            typeof seconds !== "number" ||
            Number.isNaN(seconds)
        ) {
            return;
        }

        const totalSeconds =
            Math.max(0, Math.floor(seconds));

        const days =
            Math.floor(
                totalSeconds / 86400
            );

        const hours =
            Math.floor(
                (totalSeconds % 86400) / 3600
            );

        const minutes =
            Math.floor(
                (totalSeconds % 3600) / 60
            );

        const secs =
            totalSeconds % 60;

        let text = "";

        if (days > 0) {
            text += `${days}d `;
        }

        if (hours > 0 || days > 0) {
            text += `${hours}h `;
        }

        if (minutes > 0 || hours > 0 || days > 0) {
            text += `${minutes}m `;
        }

        text += `${secs}s`;

        if (uptime) {
            uptime.textContent =
                text;
        }

        if (progress) {
            /*
             * Visual indicator only.
             * It does not represent a fake percentage.
             * It slowly approaches 100% as uptime increases.
             */
            const percentage =
                Math.min(
                    100,
                    8 +
                    Math.log10(
                        totalSeconds + 1
                    ) * 18
                );

            progress.style.width =
                `${percentage}%`;
        }
    }
};


/* =========================
   REFRESH BUTTON
========================= */

const refreshButton =
    document.getElementById(
        "refreshDashboard"
    );

if (refreshButton) {

    refreshButton.addEventListener(
        "click",
        async () => {

            refreshButton.disabled = true;

            const originalText =
                refreshButton.textContent;

            refreshButton.textContent =
                "↻ Loading...";

            try {
                await dashboard.load();
            } finally {
                refreshButton.disabled = false;

                refreshButton.textContent =
                    originalText;
            }
        }
    );
}


/* =========================
   NAVIGATION
========================= */

document.querySelectorAll(
    '.nav-links a[href^="#"]'
).forEach((link) => {

    link.addEventListener(
        "click",
        () => {

            document.querySelectorAll(
                ".nav-links a"
            ).forEach((item) => {
                item.classList.remove("active");
            });

            link.classList.add("active");
        }
    );
});


/* =========================
   INITIAL LOAD
========================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        dashboard.load();

        /*
         * Refresh real backend information
         * every 30 seconds.
         */
        setInterval(
            () => dashboard.load(),
            30000
        );
    }
);
