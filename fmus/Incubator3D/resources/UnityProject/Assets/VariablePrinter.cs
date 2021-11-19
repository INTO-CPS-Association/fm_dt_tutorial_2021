using System.Collections;
using System.Collections.Generic;

using UnityEngine;
using UnityEngine.UI;

public class VariablePrinter : MonoBehaviour
{
    public Text boxAirTemperatureText;
    public Text heatbedTemperatureText;

    private string boxAirTemperatureString = "Box Air Temperature: ";
    private string heatbedTemperatureString = "Heatbed Temperature: ";

    public double boxAirTemperature {set{this.boxAirTemperatureText.text = boxAirTemperatureString + System.Math.Round(value,2).ToString() + " C";}}
    public double heatbedTemperature {set{
        this.heatbedTemperatureText.text = heatbedTemperatureString + System.Math.Round(value,2).ToString() + " C";}}

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
