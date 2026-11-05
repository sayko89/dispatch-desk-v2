const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    // No baseUrl: Cypress serves index.html from the project root.
    specPattern: "cypress/e2e/**/*.cy.js",
    supportFile: "cypress/support/e2e.js",
    viewportWidth: 390,
    viewportHeight: 844,
    defaultCommandTimeout: 20000,
    video: true,
    videoCompression: 28,
    screenshotOnRunFailure: true,
  },
});
