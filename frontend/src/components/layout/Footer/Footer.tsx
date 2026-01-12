// frontend/src/components/layout/Footer/Footer.tsx — футер
import "./footer.css"; // 

export function Footer() {
  return (
    <footer className="footer">
      <div className="footer__inner">
        <div>© {new Date().getFullYear()} Ekaterina Fominyh</div>
      </div>
    </footer>
  );
}
