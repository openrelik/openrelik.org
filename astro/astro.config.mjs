// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// https://astro.build/config
export default defineConfig({
  site: "https://openrelik.org",
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
            { label: "Installation", slug: "docs/get-started/install" },
          ],
        },
        {
          label: "Guides",
          autogenerate: { directory: "docs/guides" },
        },
        {
          label: "Reference",
          autogenerate: { directory: "docs/reference" },
        },
      ],
      components: {
        Header: "./src/components/Header.astro",
      },
      customCss: ["./src/styles/custom.css"],
    }),
  ],
  redirects: {
    "/install.sh": {
      status: 302,
      destination:
        "https://raw.githubusercontent.com/openrelik/openrelik-deploy/main/docker/install.sh",
    },
  },
});
