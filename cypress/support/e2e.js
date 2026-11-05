// Shared commands for Dispatch Desk.
// The app runs in test mode (#test): the simulation moves 4x faster, nothing else changes.

const LIVE_LIMIT = 160;
const RIGHT = { E1: "a", E2: "a", E3: "a", E4: "b", E5: "a" }; // correct field-task answers (spec 2.5) // max polling rounds per live phase (~80 s)

// Open the intro screen, pick level / role / goal and take the shift.
// v2: the model rollout comes from the option, else from `--env rollout=on`, else the app default.
Cypress.Commands.add("startGame", ({ seviye = "orta", rol = "gelistirici", hedef = "mimari", rollout = Cypress.env("rollout") } = {}) => {
  cy.visit(rollout ? `index.html?rollout=${rollout}#test` : "index.html#test");
  cy.get(`[data-testid=seviye-${seviye}]`).check({ force: true });
  cy.get(`[data-testid=rol-${rol}]`).check({ force: true });
  cy.get(`[data-testid=hedef-${hedef}]`).check({ force: true });
  cy.get("[data-testid=basla]").click();
  cy.contains("Live dispatch").should("be.visible");
});

// Play a live dispatch phase until the alarm appears, then go to the crisis.
// pick: which option to choose on field tasks ("a" or "b"), or "right" / "wrong".
// assign: also dispatch the closest crew to waiting calls.
Cypress.Commands.add("finishLivePhase", ({ pick = "a", assign = false } = {}, round = 0) => {
  if (round > LIVE_LIMIT) throw new Error("Live phase did not reach its alarm");
  cy.get("body").then(($b) => {
    if ($b.find("[data-testid=krize-gec]").length) {
      cy.get("[data-testid=krize-gec]").click();
      return;
    }
    const open = $b.find('.event:not(.done) [data-testid^="gorev-E"]').first().attr("data-testid");
    const id = open && open.split("-")[1];
    const k = pick === "right" || pick === "wrong" ? ((RIGHT[id] === "a") === (pick === "right") ? "a" : "b") : pick;
    const taskOpt = `.event:not(.done) [data-testid="gorev-${id}-${k}"]`;
    if (id && $b.find(taskOpt).length) {
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
