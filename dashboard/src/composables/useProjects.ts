import { ref } from 'vue';
import { chatApi } from '@/api/v1';
import type { Project } from '@/components/chat/ProjectList.vue';

type WorkspaceType = 'session' | 'project' | 'custom';

function projectErrorMessage(error: unknown, fallback: string) {
    const responseMessage = (error as any)?.response?.data?.message;
    if (typeof responseMessage === 'string' && responseMessage.trim()) {
        return responseMessage;
    }
    const message = (error as Error)?.message;
    return message || fallback;
}

export function useProjects() {
    const projects = ref<Project[]>([]);
    const selectedProjectId = ref<string | null>(null);

    async function getProjects() {
        try {
            const res = await chatApi.listProjects();
            if (res.data.status === 'ok') {
                projects.value = res.data.data || [];
                
            }
        } catch (error) {
            console.error("Falha ao obter os projetos:", error);
        }
    }

    async function createProject(
        title: string,
        emoji?: string,
        description?: string,
        workspaceType: WorkspaceType = 'project',
        workspacePath?: string
    ) {
        try {
            const res = await chatApi.createProject({
                title,
                emoji: emoji || '📁',
                description,
                workspace_type: workspaceType,
                workspace_path: workspacePath
            });
            if (res.data.status === 'ok') {
                await getProjects();
                return res.data.data;
            }
            throw new Error(res.data.message || "Falha ao criar o projeto");
        } catch (error) {
            console.error("Falha ao criar o projeto:", error);
            throw new Error(projectErrorMessage(error, "Falha ao criar o projeto"));
        }
    }

    async function updateProject(
        projectId: string,
        title?: string,
        emoji?: string,
        description?: string,
        workspaceType?: WorkspaceType,
        workspacePath?: string
    ) {
        try {
            const res = await chatApi.updateProject(projectId, {
                title,
                emoji,
                description,
                workspace_type: workspaceType,
                workspace_path: workspacePath
            });
            if (res.data.status === 'ok') {
                await getProjects();
                return;
            }
            throw new Error(res.data.message || "Falha ao atualizar o projeto");
        } catch (error) {
            console.error("Falha ao atualizar o projeto:", error);
            throw new Error(projectErrorMessage(error, "Falha ao atualizar o projeto"));
        }
    }

    async function deleteProject(projectId: string) {
        try {
            const res = await chatApi.deleteProject(projectId);
            if (res.data.status === 'ok') {
                await getProjects();
                if (selectedProjectId.value === projectId) {
                    selectedProjectId.value = null;
                }
            }
        } catch (error) {
            console.error("Falha ao excluir o projeto:", error);
        }
    }

    async function addSessionToProject(sessionId: string, projectId: string) {
        try {
            const res = await chatApi.addProjectSession(projectId, sessionId);
            return res.data.status === 'ok';
        } catch (error) {
            console.error("Falha ao adicionar a sessão ao projeto:", error);
            return false;
        }
    }

    async function removeSessionFromProject(sessionId: string) {
        try {
            const res = await chatApi.removeProjectSession(sessionId);
            return res.data.status === 'ok';
        } catch (error) {
            console.error("Falha ao remover a sessão do projeto:", error);
            return false;
        }
    }

    async function getProjectSessions(projectId: string) {
        try {
            const res = await chatApi.listProjectSessions(projectId);
            if (res.data.status === 'ok') {
                return res.data.data || [];
            }
            return [];
        } catch (error) {
            console.error("Falha ao obter as sessões do projeto:", error);
            return [];
        }
    }

    return {
        projects,
        selectedProjectId,
        getProjects,
        createProject,
        updateProject,
        deleteProject,
        addSessionToProject,
        removeSessionFromProject,
        getProjectSessions
    };
}
