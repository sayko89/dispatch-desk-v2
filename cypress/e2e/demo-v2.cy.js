// Demo for the video: two players reach the same scene (Crisis 2) and the model decides differently.
// Run: npm run demo:v2  (the video lands in cypress/videos/demo-v2.cy.js.mp4)
const pause = (ms) => cy.wait(ms, { log: false });

describe("Demo v2 · same scene, two players, two model decisions", () => {
  it("Player 1 · struggling: the model offers support", () => {
    cy.startGame({ seviye: "yeni", rollout: "on" });
    cy.finishLivePhase({ pick: "wrong", assign: false });
    cy.decide(1, "a"); pause(1500); cy.continue();
    cy.finishLivePhase({ pick: "wrong", assign: false });
    cy.get("[data-testid=model-p]").should("have.attr", "data-p");
    cy.get("[data-testid=destek-kart]").scrollIntoView().should("be.visible");
    pause(4000);
  });

  it("Player 2 · steady: same scene, the model stays quiet", () => {
    cy.startGame({ seviye: "yeni", rollout: "on" });
    cy.finishLivePhase({ pick: "right", assign: true });
    cy.decide(1, "b"); pause(1500); cy.continue();
    cy.finishLivePhase({ pick: "right", assign: true });
    cy.get("[data-testid=model-p]").should("have.attr", "data-p");
    cy.get("[data-testid=destek-kart]").should("not.exist");
    cy.get("[data-testid=model-p]").scrollIntoView();
    pause(4000);
  });
});
