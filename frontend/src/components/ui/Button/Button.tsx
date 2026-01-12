// frontend/src/components/ui/Button/Button.tsx — кнопка
import "./button.css";

type Props = {
  children: React.ReactNode;
  onClick?: () => void;
  type?: "button" | "submit";
};

export function Button({ children, onClick, type = "button" }: Props) {
  return (
    <button className="btn" onClick={onClick} type={type}>
      {children}
    </button>
  );
}
