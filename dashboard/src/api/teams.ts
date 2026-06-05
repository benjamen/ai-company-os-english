import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiFetch } from './client';
import type { Team, Agent, APIResponse, APIListResponse, TeamStatus } from '../types';

export function useTeams() {
  return useQuery({
    queryKey: ['teams'],
    queryFn: () => apiFetch<APIListResponse<Team>>('/api/teams'),
  });
}

export function useTeam(id: string) {
  return useQuery({
    queryKey: ['teams', id],
    queryFn: () => apiFetch<APIResponse<Team>>(`/api/teams/${id}`),
    enabled: !!id,
  });
}

export function useTeamStatus(id: string) {
  return useQuery({
    queryKey: ['teams', id, 'status'],
    queryFn: () => apiFetch<APIResponse<TeamStatus>>(`/api/teams/${id}/status`),
    enabled: !!id,
  });
}

export function useTeamMembers(id: string) {
  return useQuery({
    queryKey: ['teams', id, 'members'],
    queryFn: () => apiFetch<APIListResponse<Agent>>(`/api/teams/${id}/members`),
    enabled: !!id,
  });
}

export function useCreateTeam() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: {
      name: string;
      mode: string;
      project_id?: string;
      leader_agent_id?: string;
      config?: Record<string, unknown>;
    }) =>
      apiFetch<APIResponse<Team>>('/api/teams', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: ['teams'] });
      if (variables.project_id) {
        void queryClient.invalidateQueries({ queryKey: ['projects', variables.project_id, 'teams'] });
      }
    },
  });
}

export function useDeleteTeam() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) =>
      apiFetch<APIResponse<null>>(`/api/teams/${id}`, { method: 'DELETE' }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['teams'] });
    },
  });
}
