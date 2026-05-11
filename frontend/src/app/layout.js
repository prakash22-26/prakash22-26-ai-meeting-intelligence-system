export const metadata = {
  title: "AI Meeting Intelligence",
  description: "AI Meeting Dashboard",
};

export default function RootLayout({ children }) {

  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}