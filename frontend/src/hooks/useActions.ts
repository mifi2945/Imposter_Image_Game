import { bindActionCreators, ActionCreatorsMapObject } from "@reduxjs/toolkit";
import { useMemo } from "react";
import { useDispatch } from "react-redux";
import type { Dispatch } from "~/redux";

export function useActions<A, M extends ActionCreatorsMapObject<A>>(actions: M) {
    const dispatch = useDispatch<Dispatch>();
    return useMemo(() => bindActionCreators(actions, dispatch), [actions, dispatch]);
}
