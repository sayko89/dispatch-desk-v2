// Shared commands for Dispatch Desk.
// The app runs in test mode (#test): the simulation moves 4x faster, nothing else changes.

const LIVE_LIMIT = 160; // max polling rounds per live phase (~80 s)

// Open the intro screen, pick level / role / goal and take the shift.
Cypress.Commands.add("startGame", ({ seviye = "orta", rol = "gelistirici", hedef = "mimari" } = {}) => {
  cy.visit("index.html#test");
  cy.get(`[data-testid=seviye-${seviye}]`).check({ force: true });
  cy.get(`[data-testid=rol-${rol}]`).check({ force: true });
  cy.get(`[data-testid=hedef-${hedef}]`).check({ force: true });
  cy.get("[data-testid=basla]").click();
  cy.contains("Live dispatch").should("be.visible");
});

// Play a live dispatch phase until the alarm appears, then go to the crisis.
// pick: which option to choose on field tasks ("a" or "b").
// assign: also dispatch the closest crew to waiting calls.
Cypress.Commands.add("finishLivePhase", ({ pick = "a", assign = false } = {}, round = 0) => {
  if (round > LIVE_LIMIT) throw new Error("Live phase did not reach its alarm");
  cy.get("body").then(($b) => {
    if ($b.find("[data-testid=krize-gec]").length) {
      cy.get("[data-testid=krize-gec]").click();
      return;
    }
    const taskOpt = `.event:not(.done) [data-testid^="gorev-E"][data-testid$="-${pick}"]`;
    if ($b.find(taskOpt).length) {
      cy.get(taskOpt).first().click({ force: true });
    } else if (assign && $b.find(".call.open [data-assign]").length) {
      cy.get(".call.open [data-assign]").first().click({ force: true });
    } else if (assign && $b.find(".call.wait:not(.open) .call-main").length) {
      cy.get(".call.wait:not(.open) .call-main").first().click({ force: true });
    } else {
      cy.wait(500, { log: false });
    }
    cy.finishLivePhase({ pick, assign }, round + 1);
  });
});

// Choose option k ("a" or "b") in crisis n and check the outcome screen.
Cypress.Commands.add("decide", (n, k) => {
  cy.get(`[data-testid=karar-${n}-${k}]`).click();
  cy.get("[data-testid=sonuc-ne-oldu]").should("be.visible");
  cy.get("[data-testid=sonuc-neden]").should("be.visible");
});

Cypress.Commands.add("continue", () => {
  cy.get("[data-testid=devam]").click();
});
