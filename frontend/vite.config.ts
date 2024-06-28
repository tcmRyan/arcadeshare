import {defineConfig} from 'vite'
import react from '@vitejs/plugin-react-swc'
import tsconfigPaths from 'vite-tsconfig-paths'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    base: '/app',
    plugins: [react(), tsconfigPaths()],
    server: {
        host: '127.0.0.1',
        port: 3000,
        proxy: {
            "/api": {
                target: 'http://127.0.0.1:5000',
                preserveHeaderKeyCase: true,
            },
            "/auth": {
                target: 'http://127.0.0.1:5000',
                changeOrigin: true,
            }
        }
    },
    resolve: {
        alias: {
            "@app": path.resolve(__dirname, "./src/app"),
            "@components": path.resolve(__dirname, "./src/components"),
            "@features": path.resolve(__dirname, "./src/features")
        },
    },
    test: {
        globals: true,
        environment: 'jsdom',
        setupFiles: './src/setupTests.ts',
        css: true,
        reporters: ['verbose'],
        coverage: {
            reporter: ["text", "json", "html"],
        },
        include: ['src/**/*'],
        exclude: [],
    }
})