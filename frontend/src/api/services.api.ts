// frontend/src/api/services.api.ts — загрузка услуг из JSON
export type Service = {
  id: number;
  slug: string;
  name: string;
  shortDescription: string;
  duration: number;
  price: number;
  description: string;
  benefits: string[];
};

export async function getServices(): Promise<Service[]> {
  const res = await fetch("/data/services.json");
  if (!res.ok) {
    throw new Error("Не удалось загрузить services_db.json");
  }
  return res.json();
}
