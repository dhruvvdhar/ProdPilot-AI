import { apiClient } from "@/api/client";
import type { APIResponse, Token, UserCreate, UserLogin, UserResponse } from "@/types";

export const authApi = {
  async register(payload: UserCreate): Promise<UserResponse> {
    const { data } = await apiClient.post<APIResponse<UserResponse>>(
      "/auth/register",
      payload,
    );
    return data.data as UserResponse;
  },

  async login(payload: UserLogin): Promise<Token> {
    const { data } = await apiClient.post<APIResponse<Token>>("/auth/login", payload);
    return data.data as Token;
  },

  async me(): Promise<UserResponse> {
    const { data } = await apiClient.get<APIResponse<UserResponse>>("/auth/me");
    return data.data as UserResponse;
  },
};
