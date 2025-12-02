function Footer() {
  return (
    <footer className="bg-slate-900 text-slate-200 py-6 mt-12">
      <div className="max-w-6xl mx-auto px-4 flex flex-col gap-2 text-sm">
        <span>© {new Date().getFullYear()} Always Free Automation.</span>
        <span>Monetização invisível via afiliados, marketplace e dados agregados.</span>
      </div>
    </footer>
  );
}

export default Footer;
