# Mantine Vite template

## Container deployment

Build and run the frontend locally from the repository root:

```sh
docker build -t frontend:local frontend
docker run --rm -p 8080:8080 frontend:local
```

Submit a Cloud Build deployment from the repository root:

```sh
gcloud builds submit --config=frontend/cloudbuild.yaml .
```

The Kubernetes Service is internal (`ClusterIP`); expose it through your
cluster's ingress or gateway to make the frontend available outside the cluster.

## API URLs

The frontend's service URL map is in `src/api/service-urls.ts`. Vite development
mode uses the local ports from the root Docker Compose setup. Non-development
builds require `VITE_ACCOUNTS_API_URL`, `VITE_FILES_API_URL`,
`VITE_LOBBY_API_URL`, `VITE_ORCHESTRATOR_API_URL`, and `VITE_QUESTIONS_API_URL`
to be set when building the frontend. These values are public URLs embedded in
the frontend bundle, so do not put secrets in them. Each API must also allow
the frontend's origin through its `CORS_ORIGINS` setting.

## Features

This template comes with the following features:

- [PostCSS](https://postcss.org/) with [mantine-postcss-preset](https://mantine.dev/styles/postcss-preset)
- [TypeScript](https://www.typescriptlang.org/)
- [Storybook](https://storybook.js.org/)
- [Vitest](https://vitest.dev/) setup with [React Testing Library](https://testing-library.com/docs/react-testing-library/intro)
- [Vite+](https://viteplus.dev/) unified toolchain: Vite, Vitest, Oxlint and Oxfmt are run with `vp` and configured in `vite.config.mjs`

## Vite+ CLI

The template works without any global installation: `vp` is installed as a dev dependency and all npm scripts use it.

Optionally, you can install the [global `vp` CLI](https://viteplus.dev/guide/global-cli).
It automatically switches to the Node.js version pinned in `.node-version` and lets you run commands directly, for example `vp dev` or `vp check --fix` instead of `yarn vp check --fix`.

## npm scripts

## Build and dev scripts

- `dev` – start development server
- `build` – build production version of the app
- `build:analyze` – build the app and open bundle size visualization (`dist/stats.html`)
- `preview` – locally preview production build

### Testing scripts

- `check` – checks formatting, lint rules and TypeScript types with `vp check`
- `check:fix` – same as `check`, fixes formatting and auto-fixable lint errors
- `typecheck` – checks TypeScript types
- `lint` – runs oxlint and stylelint
- `format:test` – checks files with oxfmt
- `vitest` – runs vitest tests
- `vitest:watch` – starts vitest watch
- `test` – runs `check`, `stylelint`, `vitest` and `build` scripts

### Other scripts

- `storybook` – starts storybook dev server
- `storybook:build` – build production storybook bundle to `storybook-static`
- `format:write` – formats all files with oxfmt
