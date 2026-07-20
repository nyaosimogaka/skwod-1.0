import api from "./axios";

export const getSports = () =>
    api.get("/api/v1/sports");

export const getSport = (id: string) =>
    api.get(`/api/v1/sports/${id}`);

export const createSport = (payload: any) =>
    api.post("/api/v1/sports", payload);

export const updateSport = (
    id: string,
    payload: any
) =>
    api.put(
        `/api/v1/sports/${id}`,
        payload
    );

export const deleteSport = (
    id: string
) =>
    api.delete(`/api/v1/sports/${id}`);