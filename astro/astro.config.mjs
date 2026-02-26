// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// https://astro.build/config
export default defineConfig({
  integrations: [
    starlight({
      title: "OpenRelik",
      logo: {
        src: "./src/assets/logo.png",
        alt: "OpenRelik Logo",
      },
      sidebar: [
        {
          label: "Get Started",
          items: [
            { label: "Overview", slug: "docs" },
            { label: "Installation", slug: "docs/install" },
          ],
        },
        {
          label: "Guides",
          autogenerate: { directory: "guides" },
        },
      ],
      components: {
        Header: "./src/components/Header.astro",
      },
      customCss: ["./src/styles/custom.css"],
    }),
  ],
});
