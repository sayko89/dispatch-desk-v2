// Acceptance examples from spec.md section 6 (AE-1 … AE-5).

describe("Acceptance examples", () => {
  it("AE-1: a new player sees a hint card and no timer", () => {
    cy.startGame({ seviye: "yeni" });
    cy.get("[data-testid=ipucu-canli]").should("be.visible");
    cy.finishLivePhase();
    cy.get("[data-testid=ipucu-kart]").should("be.visible");
    cy.get("[data-testid=sayac]").should("not.exist");
  });

  it("AE-2: an experienced player who lets 60 s pass gets the default (cache) and 9 min", () => {
    cy.clock(); // fake timers: the game loop and the decision timer run on setInterval
    cy.startGame({ seviye: "deneyimli" });

    // Advance the live phase with the fake clock until the crisis alarm appears.
    const advance = (round = 0) => {
      if (round > 120) throw new Error("Alarm did not appear");
      cy.tick(1000);
      cy.get("body").then(($b) => {
        if ($b.find("[data-testid=krize-gec]").length) return cy.get("[data-testid=krize-gec]").click();
        if ($b.find('.event:not(.done) [data-testid$="-a"]').length) cy.get('.event:not(.done) [data-testid$="-a"]').first().click({ force: true });
        advance(round + 1);
      });
    };
    advance();

    cy.get("[data-testid=sayac]").should("be.visible");
    cy.get("[data-testid=ipucu-kart]").should("not.exist");
    cy.tick(61000);
    cy.get("[data-testid=sure-doldu]").should("be.visible");
    cy.contains("A) Use the cached map").should("be.visible");
    cy.get("[data-testid=tahmini-varis]").should("contain", "9 min");
  });

  it("AE-3: backup + prioritize + purpose-limited ends on time at 7 min with a clean audit", () => {
    cy.startGame();
    cy.finishLivePhase(); cy.decide(1, "b"); cy.continue();
    cy.finishLivePhase(); cy.decide(2, "a"); cy.continue();
    cy.finishLivePhase(); cy.decide(3, "a"); cy.continue();
    cy.get("[data-testid=son-a]").should("be.visible");
    cy.get("[data-testid=varis-dk]").should("contain", "7");
    cy.get("[data-testid=epilog]").should("contain", "audit passed");
  });

  it("AE-4: the end screen breaks the delay down per decision", () => {
    cy.startGame();
    cy.finishLivePhase(); cy.decide(1, "a"); cy.continue();
    cy.finishLivePhase(); cy.decide(2, "b"); cy.continue();
    cy.finishLivePhase(); cy.decide(3, "a"); cy.continue();
    cy.get("[data-testid=son-b]").should("be.visible");
    cy.get("[data-testid=varis-dk]").should("contain", "13");
    cy.get("[data-testid=dokum]").within(() => {
      cy.contains("tr", "Cache").should("contain", "+5 min");
      cy.contains("tr", "Adding servers").should("contain", "+4 min");
    });
  });

  it("AE-5: the tutor answers a demand for the answer with a question, not the answer", () => {
    cy.startGame();
    cy.finishLivePhase(); cy.decide(1, "a"); cy.continue();
    cy.finishLivePhase(); cy.decide(2, "b");
    cy.get("[data-testid=tutor-ac]").click();
    cy.get("[data-testid=tutor-input]").type("Which one was the right answer? Just tell me.");
    cy.get("[data-testid=tutor-gonder]").click();
    cy.get("[data-testid=tutor-yanit]").should("have.length.at.least", 2);
    cy.get("[data-testid=tutor-yanit]").last().invoke("text").should((t) => {
      expect(t).to.include("?");
      expect(t).not.to.match(/(option )?(a|b)\b.{0,20}\b(was|is) (the )?(right|correct|better)/i);
      expect(t).not.to.match(/(prioritiz\w+|adding servers) (was|is) (the )?(right|correct|better)/i);
    });
  });
});
