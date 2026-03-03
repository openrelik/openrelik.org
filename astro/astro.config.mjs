// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

const googleAnalyticsId = "G-SCW4HC2P0N";

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
      head: [
        {
          tag: "script",
          attrs: {
            src: `https://www.googletagmanager.com/gtag/js?id=${googleAnalyticsId}`,
          },
        },
        {
          tag: "script",
          content: `
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', '${googleAnalyticsId}');
          `,
        },
      ],
    }),
  ],
});
