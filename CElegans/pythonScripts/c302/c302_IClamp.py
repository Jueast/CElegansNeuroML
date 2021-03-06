import c302
import sys
    
def setup(parameter_set, generate=False):

    exec('from parameters_%s import ParameterisedModel'%parameter_set)
    params = ParameterisedModel()
    
    params.set_bioparameter("unphysiological_offset_current", "0.25nA", "Testing IClamp", "0")
    params.set_bioparameter("unphysiological_offset_current_del", "100 ms", "Testing IClamp", "0")
    params.set_bioparameter("unphysiological_offset_current_dur", "800 ms", "Testing IClamp", "0")
    
    
    my_cell = "ADAL"
    
    cells               = [my_cell]
    cells_to_stimulate  = [my_cell]
    
    reference = "c302_%s_IClamp"%parameter_set
    
    if generate:
        c302.generate(reference, 
                    params, 
                    cells=cells, 
                    cells_to_stimulate=cells_to_stimulate, 
                    duration=1000, 
                    dt=0.1, 
                    validate=(parameter_set!='B'),
                    target_directory='examples')
                    
    return cells, cells_to_stimulate, params, False
             
if __name__ == '__main__':
    
    parameter_set = sys.argv[1] if len(sys.argv)==2 else 'A'
    
    setup(parameter_set, generate=True)