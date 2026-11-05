// Parity: the browser model (onnxruntime-web) must match the Python oracle within 1e-4.
// Reference values: tests/parite.json, written by `python tests/parite.py`.
describe("Model parity · browser vs Python oracle", () => {
  it("shows the same probability as Python for the 5 reference inputs", () => {
    cy.readFile("tests/parite.json").then((ref) => {
      cy.visit("index.html#test");
      cy.get("[data-testid=lab-ac]").click();
      cy.get('[data-cy="in-seviye"]', { timeout: 30000 }).should("exist");
      ref.cases.forEach((c) => {
        Object.entries(c.input).forEach(([k, v]) => cy.get(`[data-cy="in-${k}"]`).clear().type(String(v)));
        cy.get('[data-cy="p"]').invoke("removeAttr", "data-p");
        cy.get("[data-testid=lab-run]").click();
        cy.get('[data-cy="p"]').should("have.attr", "data-p").then((p) => {
          const d = Math.abs(Number(p) - c.p);
          cy.log(`${c.name}: app ${Number(p).toFixed(6)} · oracle ${c.p.toFixed(6)} · |Δ| ${d.toExponential(1)}`);
          expect(d, c.name).to.be.lessThan(ref.tolerance);
        });
      });
    });
  });
});
