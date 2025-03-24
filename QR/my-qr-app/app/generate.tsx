import React, { useState } from 'react'; 
import { View, Text, TextInput, Button, StyleSheet } from 'react-native'; 
import { Picker } from '@react-native-picker/picker'; 
import QRCode from 'react-native-qrcode-svg';
import Barcode, { Format } from 'react-native-barcode-builder';

const validFormats = ['CODE128', 'EAN', 'CODE39', 'ITF', 'MSI', 'Pharmacode', 'codabar', 'QR'] as const;
type ValidFormat = (typeof validFormats)[number];

export default function Generate() { 
  const [text, setText] = useState(''); 
  const [barcodeType, setBarcodeType] = useState<ValidFormat>('CODE128');
  const [generatedCode, setGeneratedCode] = useState<JSX.Element | null>(null);

  const validateInput = () => {
    if (!text) {
      alert('Por favor ingrese el texto para generar el código.');
      return false;
    }

    switch (barcodeType) {
      case 'EAN':
        if (text.length !== 13 && text.length !== 8) {
          alert('El código EAN debe tener 13 o 8 caracteres.');
          return false;
        }
        break;
      case 'CODE39':
        if (!/^[A-Z0-9\-\. \/\$\+%]*$/.test(text)) {
          alert('El código CODE39 solo permite letras mayúsculas, números y algunos caracteres especiales (- . $ / + %).');
          return false;
        }
        break;
      case 'codabar':
        if (!/^[A-D0-9]+$/.test(text) || text.length < 4 || text.length > 16) {
          alert('El código Codabar solo permite caracteres A-D y 0-9, con una longitud entre 4 y 16 caracteres.');
          return false;
        }
        break;
      case 'MSI':
        if (![10, 11, 18].includes(text.length)) {
          alert('El código MSI debe tener una longitud de 10, 11 o 18 caracteres.');
          return false;
        }
        break;
      case 'Pharmacode':
        if (!/^[0-9]+$/.test(text)) {
          alert('El código Pharmacode solo permite números.');
          return false;
        }
        break;
      default:
        break;
    }
    return true;
  };

  const generateCode = () => {
    if (!validateInput()) return;
    if (barcodeType === 'QR') {
      setGeneratedCode(<QRCode value={text} size={200} />);
    } else {
      setGeneratedCode(<Barcode value={text} format={barcodeType as Format} />);
    }
  };

  return ( 
    <View style={styles.container}> 
      <Text style={styles.title}>Generador de Códigos</Text> 
      <TextInput 
        style={styles.input} 
        placeholder="Ingrese el texto" 
        value={text} 
        onChangeText={setText} 
      /> 
      <Picker 
        selectedValue={barcodeType} 
        style={styles.picker} 
        onValueChange={(itemValue) => setBarcodeType(itemValue as ValidFormat)} 
      > 
        {validFormats.map((type) => (
          <Picker.Item key={type} label={`Código de ${type}`} value={type} />
        ))}
      </Picker> 
      <Button title="Generar Código" onPress={generateCode} /> 
      <View style={styles.codeContainer}> 
        {generatedCode} 
      </View> 
    </View> 
  ); 
}

const styles = StyleSheet.create({ 
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' }, 
  title: { fontSize: 24, fontWeight: 'bold' }, 
  input: { width: 250, padding: 10, marginVertical: 20, borderWidth: 1, borderRadius: 5 }, 
  picker: { width: 250, marginVertical: 20 }, 
  codeContainer: { marginTop: 20 }, 
});