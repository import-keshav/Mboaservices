import React, { useContext } from 'react';

//Client Context
export const InvigilatorContext = React.createContext({
    invigilator: null,
    clientIf: null,
    setInvigilator: (data) => { }
})

//Use Client Context
export function useInvigilatorContext() {
    return useContext(InvigilatorContext);
}
