import { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useCreateTeam } from '@/api/teams';
import { useProjectContext } from '@/context/ProjectContext';

interface CreateTeamDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  projectId?: string;
}

export function CreateTeamDialog({ open, onOpenChange, projectId }: CreateTeamDialogProps) {
  const [name, setName] = useState('');
  const [mode, setMode] = useState('coordinate');
  const [error, setError] = useState('');
  const { currentProjectId } = useProjectContext();

  const createTeam = useCreateTeam();

  // Use provided projectId or context projectId
  const effectiveProjectId = projectId || currentProjectId;

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!name.trim()) {
      setError('Team name is required');
      return;
    }

    createTeam.mutate(
      {
        name: name.trim(),
        mode,
        ...(effectiveProjectId && { project_id: effectiveProjectId }),
      },
      {
        onSuccess: () => {
          setName('');
          setMode('coordinate');
          onOpenChange(false);
        },
        onError: (err: any) => {
          if (err?.message?.includes('unique')) {
            setError('A team with this name already exists');
          } else {
            setError(err?.message || 'Failed to create team');
          }
        },
      },
    );
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <form onSubmit={handleCreate}>
          <DialogHeader>
            <DialogTitle>Create Team</DialogTitle>
            <DialogDescription>Create a new AI team for your project.</DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="team-name">Team Name *</Label>
              <Input
                id="team-name"
                placeholder="e.g., Backend Dev Team"
                value={name}
                onChange={(e) => setName(e.target.value)}
                autoFocus
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="team-mode">Team Mode</Label>
              <Select value={mode} onValueChange={setMode}>
                <SelectTrigger id="team-mode">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="coordinate">Coordinate (agents work together)</SelectItem>
                  <SelectItem value="broadcast">Broadcast (share updates)</SelectItem>
                  <SelectItem value="route">Route (sequential work)</SelectItem>
                  <SelectItem value="meet">Meet (discussion-based)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {error && <p className="text-sm text-red-600">{error}</p>}
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={createTeam.isPending}>
              {createTeam.isPending ? 'Creating...' : 'Create'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
