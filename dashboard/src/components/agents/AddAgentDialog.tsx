import { useState, useMemo } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useAllAgents } from '@/api/agents';
import { useCreateAgent } from '@/api/agents';
import { useAgents } from '@/api/agents';

interface AddAgentDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  teamId: string;
}

export function AddAgentDialog({ open, onOpenChange, teamId }: AddAgentDialogProps) {
  const [selectedAgentId, setSelectedAgentId] = useState('');
  const [error, setError] = useState('');

  const { data: allAgentsData } = useAllAgents();
  const { data: teamAgentsData } = useAgents(teamId);
  const addAgent = useCreateAgent();

  // Get agents not already in team
  const availableAgents = useMemo(() => {
    if (!allAgentsData?.data) return [];
    if (!teamAgentsData?.data) return allAgentsData.data;

    const teamAgentIds = new Set(teamAgentsData.data.map((a) => a.id));
    return allAgentsData.data.filter((a) => !teamAgentIds.has(a.id));
  }, [allAgentsData?.data, teamAgentsData?.data]);

  const handleAdd = () => {
    setError('');

    if (!selectedAgentId) {
      setError('Please select an agent');
      return;
    }

    const selectedAgent = availableAgents.find((a) => a.id === selectedAgentId);
    if (!selectedAgent) {
      setError('Selected agent not found');
      return;
    }

    addAgent.mutate(
      {
        team_id: teamId,
        name: selectedAgent.name,
        role: selectedAgent.role,
        system_prompt: selectedAgent.system_prompt,
        model: selectedAgent.model,
      },
      {
        onSuccess: () => {
          setSelectedAgentId('');
          onOpenChange(false);
        },
        onError: (err: any) => {
          setError(err?.message || 'Failed to add agent to team');
        },
      },
    );
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Add Agent to Team</DialogTitle>
          <DialogDescription>Select an agent to add to this team.</DialogDescription>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="agent-select">Available Agents</Label>
            <Select value={selectedAgentId} onValueChange={setSelectedAgentId}>
              <SelectTrigger id="agent-select">
                <SelectValue placeholder="Select an agent..." />
              </SelectTrigger>
              <SelectContent>
                {availableAgents.length === 0 ? (
                  <div className="p-2 text-sm text-gray-500">No available agents</div>
                ) : (
                  availableAgents.map((agent) => (
                    <SelectItem key={agent.id} value={agent.id}>
                      {agent.name} — {agent.role}
                    </SelectItem>
                  ))
                )}
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
          <Button onClick={handleAdd} disabled={addAgent.isPending || !selectedAgentId}>
            {addAgent.isPending ? 'Adding...' : 'Add Agent'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
