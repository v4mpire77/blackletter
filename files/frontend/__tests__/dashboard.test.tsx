import { render, screen } from "@testing-library/react";
import DashboardPage from "../app/dashboard/page";

test("renders dashboard UI", () => {
  render(<DashboardPage />);
  expect(screen.getByText(/Compliance Dashboard/)).toBeInTheDocument();
});