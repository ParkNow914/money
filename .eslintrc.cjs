module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2021: true,
  },
  parser: "@typescript-eslint/parser",
  parserOptions: {
    project: false,
    ecmaFeatures: {
      jsx: true,
    },
  },
  plugins: ["@typescript-eslint", "import", "react", "react-hooks"],
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "plugin:import/recommended",
    "plugin:import/typescript",
    "prettier",
  ],
  settings: {
    "import/resolver": {
      node: {
        extensions: [".js", ".jsx", ".ts", ".tsx"],
      },
    },
    react: {
      version: "detect",
    },
  },
  rules: {
    "@typescript-eslint/no-explicit-any": "off",
    "import/no-unresolved": "off",
    "import/order": [
      "warn",
      {
        groups: [["builtin", "external"], ["internal"], ["parent", "sibling", "index"]],
        "newlines-between": "always",
      },
    ],
    "react/react-in-jsx-scope": "off",
  },
};
