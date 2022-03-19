import { defineConfig } from "vite";
import { resolve } from "path";
import fs from "fs/promises";
// https://vitejs.dev/config/
export default defineConfig({
  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:6000",
        changeOrigin: true,
      },
      "/video": {
        target: "http://172.20.10.2:8080",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/video/, ""),
      },
    },
  },
  resolve: {
    alias: {
      src: resolve(__dirname, "src"),
    },
  },
  esbuild: {
    loader: "jsx",
    include: /src\/.*\.jsx?$/,
    exclude: [],
  },
  optimizeDeps: {
    esbuildOptions: {
      plugins: [
        {
          name: "load-js-files-as-jsx",
          setup(build) {
            build.onLoad({ filter: /src\\.*\.js$/ }, async (args) => ({
              loader: "jsx",
              contents: await fs.readFile(args.path, "utf8"),
            }));
          },
        },
      ],
    },
  },
});
