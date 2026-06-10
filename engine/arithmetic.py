def eval_expr(expr, vars):
    try:
        for name in vars.table:
            expr = expr.replace(name, str(vars.get(name)))
        return eval(expr)
    except Exception as e:
        raise Exception(f"Invalid arithmetic: {expr}")
