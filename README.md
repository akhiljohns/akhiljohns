### Hi there, I'm Akhil Johns 👋

I'm a full-stack developer from Kerala, India, with a passion for building scalable, high-quality web applications. I enjoy working across the entire stack, from designing intuitive user interfaces to architecting robust backend systems.

---
## 🌐 Socials
[![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?logo=Instagram&logoColor=white)](https://instagram.com/_akhil_johns__) [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/akhil-johns) [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/akhiljohns3) [![email](https://img.shields.io/badge/Email-D14836?logo=gmail&logoColor=white)](mailto:akhiljohns.dev@gmail.com) 

---

## My Evolution as a Developer
I'm a firm believer in continuous improvement. Over the past few years, I've transitioned from foundational MERN stack development to building scalable, enterprise-grade applications. This journey has taught me the importance of architecture, code quality, and maintainability. 

Below is a summary of the core principles that guide my work today, ensuring every project I build is performant, scalable, and a pleasure to maintain.

---

## My Modern Development Playbook

### 1. Architecture: Feature-Sliced for Scalability
I've moved from traditional folder-by-type organization to a **feature-sliced architecture**. This keeps features self-contained and makes the codebase easier to scale and maintain, especially in a team environment.
```
src/
├── app/
│   ├── pages/              # Page-level components
│   │   ├── customers/      # Customer feature
│   │   │   ├── api/        # API layer
│   │   │   ├── components/ # Feature-specific components
│   │   │   ├── hooks/      # Custom hooks
│   │   │   └── types/      # TypeScript types
│   │   └── ...other-features
│   └── router.tsx          # Centralized routing
├── components/
│   ├── ui/                 # Reusable UI primitives (shadcn)
│   └── layouts/            # Layout components
└── stores/                 # Global state (Zustand)
```

### 2. State Management: The Right Tool for the Job
I use a hybrid approach to state, separating server state from UI state.
-   **Server State (TanStack Query):** For all API interactions, I use TanStack Query to handle caching, background refetching, and request deduplication automatically. This keeps the UI fast and responsive.
-   **Client State (Zustand):** For global UI state like themes or authentication status, I use Zustand. It's lightweight, requires minimal boilerplate, and doesn't need a context provider.
-   **Form State (React Hook Form + Zod):** For complex forms, I combine React Hook Form with Zod for robust, type-safe validation from schema.

### 3. UI Development: Accessible & Type-Safe
My UI development is centered around building accessible and maintainable component systems.
-   **Component Library:** I build with **shadcn/ui**, based on unstyled **Radix UI** primitives, ensuring that all components are WCAG 2.1 AA compliant from the start.
-   **Styling:** I use **Tailwind CSS** for utility-first styling, and **CVA** to create type-safe component variants.

### 4. Code Quality: Strict & Automated
I enforce high code quality standards through automation.
-   **TypeScript-First:** All projects are built with a `strict` TypeScript configuration.
-   **Linting & Formatting:** I use **ESLint** and **Prettier** with pre-commit hooks to ensure all code is consistent, error-free, and well-formatted before it ever enters the codebase.
-   **CI/CD:** Type checking and linting are always part of the CI/CD pipeline on **GitHub Actions**.

---
# 📊 GitHub Stats & Activity

![](https://github-readme-stats.vercel.app/api?username=akhiljohns&theme=blue_navy&hide_border=false&include_all_commits=true&count_private=true)<br/>
![](https://nirzak-streak-stats.vercel.app/?user=akhiljohns&theme=blue_navy&hide_border=false)<br/>
![](https://github-readme-stats.vercel.app/api/top-langs/?username=akhiljohns&theme=blue_navy&hide_border=false&include_all_commits=true&count_private=true&layout=compact)

### 🔝 Top Contributed Repo
![](https://github-contributor-stats.vercel.app/api?username=akhiljohns&limit=5&theme=github_dark&combine_all_yearly_contributions=true)

---
[![](https://visitcount.itsvg.in/api?id=akhiljohns&icon=1&color=0)](https://visitcount.itsvg.in)


