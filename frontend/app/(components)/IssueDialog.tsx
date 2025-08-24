import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import type { Issue } from "@/types/review";

interface Props {
  issue: Issue;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export default function IssueDialog({ issue, open, onOpenChange }: Props) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{issue.description}</DialogTitle>
        </DialogHeader>
        <pre>{issue.citation || "No citation"}</pre>
      </DialogContent>
    </Dialog>
  );
}
