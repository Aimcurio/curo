# Adapter Contract

## Purpose

Adapters isolate model-specific or provider-specific differences from the portable operating standard.

## Requirements

- preserve the raw provider interaction where feasible
- do not overwrite canonical evidence with inferred summaries
- expose structured inputs and outputs
- keep provider quirks out of policy logic

## Boundary

Adapters may translate formats. They may not change truth ownership.

