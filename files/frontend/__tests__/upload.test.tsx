import { render, screen, fireEvent } from "@testing-library/react";
import UploadPage from "../app/upload/page";

test("renders upload UI", () => {
  render(<UploadPage />);
  expect(screen.getByText(/Upload Contract/)).toBeInTheDocument();
});