import os

BASE = "frontend"

structure = [
    "app/(auth)/login",
    "app/(auth)/register",

    "app/(dashboard)/classes",
    "app/(dashboard)/bookings",
    "app/(dashboard)/admin",

    "app",

    "lib",
    "store",
    "types",
    "components/ui",
    "components/layout",
    "components/shared",
    "hooks",
    "services",
]

files = [
    "app/layout.tsx",
    "app/page.tsx",

    "app/(dashboard)/layout.tsx",

    "lib/api.ts",
    "lib/auth.ts",
    "lib/endpoints.ts",

    "store/auth-store.ts",

    "types/auth.ts",
    "types/class.ts",
    "types/booking.ts",

    "hooks/useAuth.ts",
    "hooks/useClasses.ts",

    "services/auth.service.ts",
    "services/class.service.ts",
    "services/booking.service.ts",

    "middleware.ts",
    ".env.local",
]


def create_folder(path):
    full_path = os.path.join(BASE, path)
    os.makedirs(full_path, exist_ok=True)
    print(f"📁 created: {full_path}")


def create_file(path):
    full_path = os.path.join(BASE, path)

    if not os.path.exists(full_path):
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("")
        print(f"📄 created: {full_path}")
    else:
        print(f"⏭ exists: {full_path}")


def main():
    print("\n🚀 Frontend structure creating...\n")

    for folder in structure:
        create_folder(folder)

    for file in files:
        create_file(file)

    print("\n✅ Done!")


if __name__ == "__main__":
    main()