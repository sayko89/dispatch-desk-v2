// All 8 decision paths (spec.md section 2.4).
// Arrival minutes = 4 base + crisis 1 (cache +5, backup +3) + crisis 2 (prioritize +0, add servers +4).
// Ending A when arrival <= 10. Crisis 3 decides the epilog.

const PATHS = [
  { id: "P1", k: ["a", "a", "a"], min: 9, end: "son-a", audit: "passed" },
  { id: "P2", k: ["a", "a", "b"], min: 9, end: "son-a", audit: "found raw" },
  { id: "P3", k: ["a", "b", "a"], min: 13, end: "son-b", audit: "passed" },
  { id: "P4", k: ["a", "b", "b"], min: 13, end: "son-b", audit: "found raw" },
  { id: "P5", k: ["b", "a", "a"], min: 7, end: "son-a", audit: "passed" },
  { id: "P6", k: ["b", "a", "b"], min: 7, end: "son-a", audit: "found raw" },
  { id: "P7", k: ["b", "b", "a"], min: 11, end: "son-b", audit: "passed" },
  { id: "P8", k: ["b", "b", "b"], min: 11, end: "son-b", audit: "found raw" },
];

describe("Decision paths", () => {
  PATHS.forEach((p) => {
    it(`${p.id}: ${p.k.join("-").toUpperCase()} ends ${p.end === "son-a" ? "on time" : "delayed"} at ${p.min} min`, () => {
      cy.startGame();

      cy.finishLivePhase();
      cy.decide(1, p.k[0]);
      cy.continue();

      cy.finishLivePhase();
      cy.decide(2, p.k[1]);
      cy.continue();

      cy.finishLivePhase();
      cy.decide(3, p.k[2]);
      cy.continue();

      cy.get(`[data-testid=${p.end}]`).should("be.visible").and("contain", `Path ${p.id}`);
      cy.get("[data-testid=varis-dk]").should("contain", String(p.min));
      cy.get("[data-testid=dokum]").should("contain", `Total`).and("contain", `${p.min} min`);
      cy.get("[data-testid=epilog]").should("contain", p.audit);
      cy.get("[data-testid=karne]").should("be.visible");
    });
  });
});
