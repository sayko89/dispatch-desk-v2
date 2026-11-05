// About 60 seconds of gameplay for the demo video: dispatching crews, field tasks,
// all three crises and the end screen. Run with: npm run demo
// The video is saved to cypress/videos/demo.cy.js.mp4

describe("Demo run", () => {
  it("plays one full shift (path P5)", () => {
    cy.startGame({ seviye: "yeni", hedef: "olcek" });
    cy.finishLivePhase({ assign: true });
    cy.wait(1500);
    cy.decide(1, "b");
    cy.wait(2500);
    cy.continue();

    cy.finishLivePhase({ assign: true });
    cy.wait(1500);
    cy.decide(2, "a");
    cy.wait(2500);
    cy.get("[data-testid=tutor-ac]").click();
    cy.wait(2000);
    cy.get("[data-testid=tutor-kapat]").click();
    cy.continue();

    cy.finishLivePhase({ assign: true, pick: "b" });
    cy.wait(1500);
    cy.decide(3, "a");
    cy.wait(2000);
    cy.continue();

    cy.get("[data-testid=son-a]").should("be.visible");
    cy.wait(1500);
    cy.get("[data-testid=karne]").scrollIntoView({ duration: 2000 });
    cy.wait(2500);
  });
});
