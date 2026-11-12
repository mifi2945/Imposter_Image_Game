import { bindActionCreators, ActionCreatorsMapObject } from "@reduxjs/toolkit";
import { useDispatch } from "react-redux";
import type { Dispatch } from "~/redux";

export function useActions<A, M extends ActionCreatorsMapObject<A>>(actions: M) {
    return bindActionCreators(actions, useDispatch<Dispatch>());
}
