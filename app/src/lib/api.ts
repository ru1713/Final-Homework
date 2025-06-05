import axios from "axios";

/**
 * 共通 axios インスタンス
 * baseURL は FastAPI が動いているポート 8000
 */
export const api = axios.create({
  baseURL: "http://localhost:8000",
});
