// v2 acceptance examples AE-6, AE-7 and AE-8 (spec.md, section 11.6). The model is switched on with ?rollout=on.
const toCrisis3 = (level, { pick, assign, choices }) => {
  cy.startGame({ seviye: level, rollout: "on" });
  cy.finishLivePhase({ pick, assign });
  cy.decide(1, choices[0]); cy.continue();
  cy.finishLivePhase({ pick, assign });
  cy.decide(2, choices[1]); cy.continue();
  cy.finishLivePhase({ pick, assign });
};

describe("v2 · model changes the game", () => {
  it("AE-6 · a struggling player gets support", () => {
    toCrisis3("yeni", { pick: "wrong", assign: false, choices: ["a", "b"] });
    cy.get("[data-testid=model-p]").should("have.attr", "data-p").then((p) => expect(Number(p)).to.be.at.least(0.5));
    cy.get("[data-testid=destek-kart]").should("be.visible");
    cy.decide(3, "a");
    cy.get("[data-testid=sonuc-derin]").should("be.visible"); // expanded explanation for a supported crisis
  });

  it("AE-7 · a steady player gets no support", () => {
    toCrisis3("deneyimli", { pick: "right", assign: true, choices: ["b", "a"] });
    cy.get("[data-testid=model-p]").should("have.attr", "data-p").then((p) => expect(Number(p)).to.be.below(0.5));
    cy.get("[data-testid=destek-kart]").should("not.exist");
  });

  it("AE-8 · no model, no change", () => {
    cy.intercept("GET", "**/model/**", { forceNetworkError: true });
    cy.intercept("GET", "https://huggingface.co/**", { forceNetworkError: true });
    cy.startGame({ seviye: "yeni", rollout: "on" });
    cy.finishLivePhase({ pick: "wrong" });
    cy.get("[data-testid=model-p]").should("contain", "Model offline · v1 rules");
    cy.get("[data-testid=destek-kart]").should("not.exist");
    cy.get("[data-testid=ipucu-kart]").should("be.visible"); // v1 rule for a new player still holds
  });
});
