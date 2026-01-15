// frontend/src/pages/Admin/ServicesPage.tsx — управление услугами
// Назначение: просмотр, редактирование, создание и удаление услуг (админка)

import { useEffect, useState } from "react";
import "./admin.css";

type Service = {
  id: number;
  name: string;
  price: number;
  duration_minutes: number | null;
};

export function ServicesPage() {
  const userId = localStorage.getItem("user_id");

  const [services, setServices] = useState<Service[]>([]);
  const [editId, setEditId] = useState<number | null>(null);
  const [draft, setDraft] = useState<Partial<Service>>({});

  const [isCreating, setIsCreating] = useState(false); // (я добавил)
  const [createDraft, setCreateDraft] = useState<Partial<Service>>({}); // (я добавил)

  const loadServices = async () => {
    const r = await fetch("/api/admin/services", {
      headers: { "X-User-Id": userId! },
    });
    const data = await r.json();
    setServices(Array.isArray(data) ? data : []);
  };

  useEffect(() => {
    loadServices();
  }, []);

  const startEdit = (s: Service) => {
    setEditId(s.id);
    setDraft({ ...s });
  };

  const cancelEdit = () => {
    setEditId(null);
    setDraft({});
  };

  const saveEdit = async () => {
    if (!window.confirm("Сохранить изменения?")) return;

    await fetch(`/api/admin/services/${editId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-User-Id": userId!,
      },
      body: JSON.stringify(draft),
    });

    cancelEdit();
    loadServices();
  };

  const deleteService = async (id: number) => {
    if (!window.confirm("Удалить услугу?")) return;

    await fetch(`/api/admin/services/${id}`, {
      method: "DELETE",
      headers: { "X-User-Id": userId! },
    });

    loadServices();
  };

  const createService = async () => {
    if (!createDraft.name || !createDraft.price) {
      alert("Заполните название и цену");
      return;
    }

    await fetch("/api/admin/services", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-User-Id": userId!,
      },
      body: JSON.stringify(createDraft),
    });

    setIsCreating(false);
    setCreateDraft({});
    loadServices();
  };

  return (
    <div className="admin">
      <div className="admin__header"> {/* (я добавил) */}
        <h1 className="admin__h1">Услуги</h1>
        {!isCreating && (
          <button
            className="btn btn--primary"
            onClick={() => setIsCreating(true)}
          >
            + Добавить услугу
          </button>
        )}
      </div>

      <div className="table">
        <div className="table__head">
          <div>Название</div>
          <div>Цена</div>
          <div>Минут</div>
          <div />
        </div>

        {isCreating && (
          <div className="table__row table__row--edit"> {/* (я добавил) */}
            <input
              className="input input--table"
              placeholder="Название услуги"
              value={createDraft.name ?? ""}
              onChange={(e) =>
                setCreateDraft({ ...createDraft, name: e.target.value })
              }
            />

            <input
              className="input input--table"
              type="number"
              placeholder="Цена"
              value={createDraft.price ?? ""}
              onChange={(e) =>
                setCreateDraft({
                  ...createDraft,
                  price: Number(e.target.value),
                })
              }
            />

            <input
              className="input input--table"
              type="number"
              placeholder="Минут"
              value={createDraft.duration_minutes ?? ""}
              onChange={(e) =>
                setCreateDraft({
                  ...createDraft,
                  duration_minutes: Number(e.target.value),
                })
              }
            />

            <div className="table__actions">
              <button
                className="btn btn--primary"
                onClick={createService}
              >
                Создать
              </button>
              <button
                className="btn btn--ghost"
                onClick={() => {
                  setIsCreating(false);
                  setCreateDraft({});
                }}
              >
                Отмена
              </button>
            </div>
          </div>
        )}

        {services.map((s) => {
          const isEdit = editId === s.id;

          return (
            <div
              key={s.id}
              className={`table__row ${
                isEdit ? "table__row--edit" : ""
              }`}
            >
              <input
                className="input input--table"
                disabled={!isEdit}
                value={isEdit ? draft.name ?? "" : s.name}
                onChange={(e) =>
                  setDraft({ ...draft, name: e.target.value })
                }
              />

              <input
                className="input input--table"
                type="number"
                disabled={!isEdit}
                value={isEdit ? draft.price ?? 0 : s.price}
                onChange={(e) =>
                  setDraft({
                    ...draft,
                    price: Number(e.target.value),
                  })
                }
              />

              <input
                className="input input--table"
                type="number"
                disabled={!isEdit}
                value={
                  isEdit
                    ? draft.duration_minutes ?? ""
                    : s.duration_minutes ?? ""
                }
                onChange={(e) =>
                  setDraft({
                    ...draft,
                    duration_minutes: Number(e.target.value),
                  })
                }
              />

              {!isEdit ? (
                <button
                  className="btn btn--ghost"
                  onClick={() => startEdit(s)}
                >
                  Редактировать
                </button>
              ) : (
                <div className="table__actions">
                  <button
                    className="btn btn--primary"
                    onClick={saveEdit}
                  >
                    Сохранить
                  </button>
                  <button
                    className="btn btn--ghost"
                    onClick={cancelEdit}
                  >
                    Отмена
                  </button>
                  <button
                    className="btn btn--danger"
                    onClick={() => deleteService(s.id)}
                  >
                    Удалить
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
