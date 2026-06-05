import { Badge } from '@/components/ui/badge';

interface AgentStatusBadgeProps {
  status: string;
}

export function AgentStatusBadge({ status }: AgentStatusBadgeProps) {
  const statusLower = status.toLowerCase();

  if (statusLower === 'waiting') {
    return <Badge className="bg-green-100 text-green-800">Waiting</Badge>;
  }

  if (statusLower === 'busy') {
    return <Badge className="bg-blue-100 text-blue-800">Busy</Badge>;
  }

  if (statusLower === 'offline') {
    return <Badge className="bg-gray-100 text-gray-800">Offline</Badge>;
  }

  return <Badge variant="outline">{status}</Badge>;
}
